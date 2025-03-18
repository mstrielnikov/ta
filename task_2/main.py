from cli import *
from blockchain import *
from sys import exit
from os import getenv
from dotenv import load_dotenv


load_dotenv()

WEB3_PROVIDER_URL = getenv("WEB3_PROVIDER_URL")
if not WEB3_PROVIDER_URL:
    raise ValueError("WEB3_PROVIDER_URL is not set in the .env file")

parser = setup_argparse()
args = parser.parse_args()

if not args.command:
    parser.print_help()
    exit(0)

try:
    # Initialize the explorer
    web3_provider = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
    if not web3_provider.is_connected():
        raise Exception("Failed to connect to Ethereum node")

    explorer = BlockchainExplorer(web3_provider)
    print("Connected to Ethereum node successfully!")

    if args.command == "block-number":
        block_number = explorer.get_latest_block_number()
        if block_number is not None:
            print(f"Latest block number: {block_number}")

    elif args.command == "block-transactions":
        block_number = args.block if args.block else explorer.get_latest_block_number()
        if block_number is not None:
            print(f"Fetching transactions for block {block_number}...")
            transactions = explorer.get_block_transactions(block_number)
            if transactions:
                print(f"Found {len(transactions)} transactions:")
                for i, tx in enumerate(transactions, 1):
                    print(f"\nTransaction {i}:")
                    print(f"Hash: {tx['hash']}")
                    print(f"From: {tx['from']}")
                    print(f"To: {tx['to']}")
                    print(f"Value: {tx['value']} ETH")
                    print(f"Gas: {tx['gas']}")
                    print(f"Gas Price: {tx['gas_price']} Gwei")

    elif args.command == "balance":
        balance = explorer.get_address_balance(args.address)
        if balance is not None:
            print(f"Balance of {args.address}: {balance} ETH")

except Exception as e:
    print(f"An error occurred: {e}")
