from web3 import Web3
import os
from dotenv import load_dotenv
from transfers import *

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Configuration from .env
    WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL")
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
    ADDRESS_TO_ANALYZE = os.getenv("ADDRESS_TO_ANALYZE")

    # Validate environment variables
    if not WEB3_PROVIDER_URL:
        raise ValueError("WEB3_PROVIDER_URL is not set in the .env file")
    if not CONTRACT_ADDRESS:
        raise ValueError("CONTRACT_ADDRESS is not set in the .env file")
    if not ADDRESS_TO_ANALYZE:
        raise ValueError("ADDRESS_TO_ANALYZE is not set in the .env file")

    # Connect to Ethereum network
    web3_api = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
    if not web3_api.is_connected():
        raise Exception("Failed to connect to Ethereum network")

    with open("./rpc_transfers.json") as abi:
        CONTRACT_ABI: str = abi.read() # type annotations allows to ensure it's not None
        transfers_contract = web3_api.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
        analyze_token_transfers(web3_api, transfers_contract, ADDRESS_TO_ANALYZE)