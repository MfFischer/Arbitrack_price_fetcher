# backend/arbitrage_bot.py

import logging
import json
from decimal import Decimal, getcontext


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class PriceFetcher:
    def __init__(self, exchange_urls):
        self.exchange_urls = exchange_urls

    async def fetch_price(self, session, exchange_name, pair):
        url = self.exchange_urls.get(exchange_name)
        query = self._construct_graphql_query(pair)
        logger.debug(f"Constructed GraphQL query for {exchange_name}: {query}")

        try:
            async with session.post(url, json={"query": query}) as response:
                response.raise_for_status()
                data = await response.json()
                if 'errors' in data:
                    logger.error(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
                    return None
                pools = data.get('data', {}).get('pools', [])
                if not pools:
                    logger.warning(f"No pools data found in response from {exchange_name}.")
                    return None
                logger.debug(f"Received pools data from {exchange_name}: {json.dumps(pools, indent=2)}")
                return pools
        except Exception as e:
            logger.error(f"Unexpected error in fetch_price: {str(e)}")
            logger.exception("Full traceback:")
            return None

    def _construct_graphql_query(self, pair):
        token0 = pair['token0']
        token1 = pair['token1']
        feeTier = pair['feeTier'] if pair.get('feeTier') else ""

        query = f"""
        {{
            pools(
                where: {{
                    feeTier: {feeTier},
                    token0_in: ["{token0}", "{token1}"],
                    token1_in: ["{token0}", "{token1}"]
                }}
            ) {{
                id
                token0 {{
                    id
                    symbol
                }}
                token1 {{
                    id
                    symbol
                }}
                sqrtPrice
                liquidity
                feeTier
            }}
        }}
        """
        return query

    def _find_matching_pool(self, pools, pair):
        matching_pools = []
        for pool in pools:
            token0_id = pool['token0']['id'].lower()
            token1_id = pool['token1']['id'].lower()
            if ((token0_id == pair['token0'] and token1_id == pair['token1']) or
                (token0_id == pair['token1'] and token1_id == pair['token0'])):
                matching_pools.append(pool)
        if matching_pools:
            matching_pools.sort(key=lambda x: int(x['liquidity']), reverse=True)
            return matching_pools[0]
        return None

    def _compute_price_from_sqrtPriceX96(self, sqrtPriceX96, pool_token0_id, pool_token1_id, pair):
        getcontext().prec = 60  # High decimal precision for accurate calculation

        # Debugging to ensure we have correct types and values
        logger.debug(f"Type of sqrtPriceX96: {type(sqrtPriceX96)}, Value: {sqrtPriceX96}")

        if isinstance(sqrtPriceX96, list):
            logger.error(f"Expected a single value for sqrtPriceX96, but got a list: {sqrtPriceX96}")
            sqrtPriceX96 = sqrtPriceX96[0]  # Optionally take the first element

        sqrtPriceX96 = Decimal(sqrtPriceX96)
        Q96 = Decimal(2 ** 96)

        price = (sqrtPriceX96 / Q96) ** 2
        if pool_token0_id.lower() == pair['token0']:
            return float(price)
        else:
            return float(1 / price)

    async def compare_prices(self, session, pairs_and_fee_tiers):
        results = []

        for pair in pairs_and_fee_tiers:
            exchange1_data = await self.fetch_price(session, 'exchange1', pair)
            exchange2_data = await self.fetch_price(session, 'exchange2', pair)

            if exchange1_data and exchange2_data:
                pool1 = self._find_matching_pool(exchange1_data, pair)
                pool2 = self._find_matching_pool(exchange2_data, pair)

                if pool1 and pool2:
                    token0 = pool1['token0']['symbol']
                    token1 = pool1['token1']['symbol']

                    sqrtPrice1 = int(pool1['sqrtPrice'])
                    sqrtPrice2 = int(pool2['sqrtPrice'])

                    price1 = self._compute_price_from_sqrtPriceX96(sqrtPrice1, pool1['token0']['id'], pool1['token1']['id'], pair)
                    price2 = self._compute_price_from_sqrtPriceX96(sqrtPrice2, pool2['token0']['id'], pool2['token1']['id'], pair)

                    liquidity = int(pool1['liquidity'])

                    if price1 > 0 and price2 > 0:
                        price_diff_percentage = abs(price1 - price2) / min(price1, price2) * 100
                    else:
                        price_diff_percentage = None

                    result = {
                        "pool_id": pool1['id'],
                        "token0": token0,
                        "token1": token1,
                        "exchange1_price": price1,
                        "exchange2_price": price2,
                        "liquidity": liquidity,
                        "feeTier": pool1['feeTier'],
                        "price_difference_percentage": round(price_diff_percentage, 2) if price_diff_percentage is not None else "N/A",
                        "buy_on_exchange": "exchange1" if price1 < price2 else "exchange2"
                    }
                    results.append(result)
                else:
                    logger.warning(f"Could not find matching pools for pair {pair} in one or both exchanges.")
            else:
                logger.warning(f"Could not fetch data for pair {pair} from one or both exchanges.")

        return results
