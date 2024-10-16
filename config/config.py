# config/config.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"

    GRAPH_API_KEY = os.getenv("GRAPH_API_KEY")
    EXCHANGE_1_SUBGRAPH_ID = os.getenv("EXCHANGE_1_SUBGRAPH_ID", "9fWsevEC9Yz4WdW9QyUvu2JXsxyXAxc1X4HaEkmyyc75")
    EXCHANGE_2_SUBGRAPH_ID = os.getenv("EXCHANGE_2_SUBGRAPH_ID", "7okunX6MGm2pdFK7WJSwm9o82okpBLEzfGrqHDDMWYvq")

    GRAPH_ENDPOINT_TEMPLATE = "https://gateway.thegraph.com/api/{api_key}/subgraphs/id/{subgraph_id}"

    @staticmethod
    def get_graph_url(api_key, subgraph_id):
        return Config.GRAPH_ENDPOINT_TEMPLATE.format(api_key=api_key, subgraph_id=subgraph_id)
