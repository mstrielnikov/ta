from web3 import Web3
import solcx
import os
from dotenv import load_dotenv
from json import dumps as jsonify
from json import loads as jsonloads
from helpers import *


# Load environment variables
load_dotenv()

# Configuration
WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
SMARTCONTRACT_FILENAME="Election.sol"
SOLIDITY_CONTRACT_PATH = os.getenv("SOLIDITY_CONTRACT_PATH", f"../contracts/{SMARTCONTRACT_FILENAME}")
ARTIFACT_OUTPUT_PATH = os.getenv("ARTIFACT_OUTPUT_PATH", "../artifacts/voting_contract.json")
SOLIDITY_VERSION = "0.8.2"

# Validate environment variables
if not WEB3_PROVIDER_URL:
    raise ValueError("WEB3_PROVIDER_URL is not set in the .env file")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY is not set in the .env file")
if not ACCOUNT_ADDRESS:
    raise ValueError("ACCOUNT_ADDRESS is not set in the .env file")
if not os.path.exists(SOLIDITY_CONTRACT_PATH):
    raise FileNotFoundError(f"Solidity contract file not found: {SOLIDITY_CONTRACT_PATH}")

ACCOUNT_ADDRESS = Web3.to_checksum_address(ACCOUNT_ADDRESS)

w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
print(f"Connected to Sepolia: {w3.is_connected()}")
if not w3.is_connected():
    raise Exception("Failed to connect to the Ethereum testnet")
print(f"Chain ID: {w3.eth.chain_id}")
print(f"Account balance: {w3.eth.get_balance(ACCOUNT_ADDRESS)} wei")

account = w3.eth.account.from_key(PRIVATE_KEY)
w3.eth.default_account = account.address

try:
    solcx.install_solc(SOLIDITY_VERSION)
    # print(f"Installed solc version: {solcx.get_solc_version()}")
except Exception as e:
    print(f"Failed to install solc: {e}")
    print("Available versions:", solcx.get_installable_solc_versions())
    raise

contract_content = read_file(SOLIDITY_CONTRACT_PATH)

compiled_sol = solcx_compile(SMARTCONTRACT_FILENAME, contract_content, SOLIDITY_VERSION)

bytecode = compiled_sol["contracts"]["Election.sol"]["Voting"]["evm"]["bytecode"]["object"]
print("Compiled solidity contract bytecode:")
print(bytecode)
print(50 * "=")

abi = jsonloads(compiled_sol["contracts"][SMARTCONTRACT_FILENAME]["Voting"]["metadata"])["output"]["abi"]
print(jsonify(abi))
print(50 * "=")

contract_address = deploy_contract_tx(w3, account, PRIVATE_KEY, abi, bytecode)

# Save the contract address and ABI for later use
with open(ARTIFACT_OUTPUT_PATH, "w") as f:
    json_data = {"address": contract_address, "abi": abi}
    f.write(jsonify(json_data))
