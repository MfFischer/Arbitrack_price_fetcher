# backend/app.py
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, render_template, send_from_directory
from arbitrage_bot import PriceFetcher
import aiohttp
import asyncio
# Import the configuration from the config folder
from config.config import Config

app = Flask(
    __name__,
    static_folder="static",      # Serve static files from frontend/static
    template_folder="../frontend/templates"  # Serve templates (HTML) from frontend/templates
)


@app.route('/')
def index():
    # Render index.html to ensure Jinja2 template tags are processed
    return render_template('index.html')

app.route('/test-static')
def test_static():
    return send_from_directory(app.static_folder, 'styles.css')


@app.route('/fetch-prices', methods=['POST'])
async def fetch_prices():
    data = request.get_json()
    api_key = data.get('apiKey') or Config.GRAPH_API_KEY
    subgraph_id1 = data.get('subgraphId1') or Config.EXCHANGE_1_SUBGRAPH_ID
    subgraph_id2 = data.get('subgraphId2') or Config.EXCHANGE_2_SUBGRAPH_ID

    exchange_urls = {
        'exchange1': Config.get_graph_url(api_key, subgraph_id1),
        'exchange2': Config.get_graph_url(api_key, subgraph_id2)
    }

    pairs_and_fee_tiers = [{
        "token0": data.get('token1').lower(),
        "token1": data.get('token2').lower(),
        "feeTier": data.get('feeTier')
    }]

    fetcher = PriceFetcher(exchange_urls)

    async with aiohttp.ClientSession() as session:
        results = await fetcher.compare_prices(session, pairs_and_fee_tiers)

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=Config.DEBUG)
