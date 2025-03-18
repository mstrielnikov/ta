from web3 import Web3
from web3.contract import Contract  # Import Contract type
from datetime import datetime
from typing import Union


# Retrieve Transfer event logs from the contract.
def get_logs_transfer(contract: Contract, contract_address: str, from_block: int, to_block: Union[int, str] = "latest"):
    try:
        logs = contract.events.Transfer.get_logs(
            fromBlock=from_block,
            toBlock=to_block,
            argument_filters={"from": contract_address}  # Filter by sender
        )
        return logs
    except Exception as e:
        print(f"Error retrieving Transfer logs: {e}")
        return []


def analyze_token_transfers(web3_api: Web3, contract: Contract, contract_address: str):
    """
    Analyze token transfers for a given address.
    """
    # Define block range to analyze (e.g., last 1000 blocks or specific range)
    latest_block = web3_api.eth.block_number
    from_block = latest_block - 1000  # Adjust this range as needed

    # Get Transfer events where contract_address is the sender
    transfer_logs = get_logs_transfer(contract, contract_address, from_block)

    # Variables to store analysis results
    total_transfers = 0
    total_amount_sent = 0
    transfer_details = []

    print(f"\nAnalyzing token transfers from block {from_block} to {latest_block}...")
    for log in transfer_logs:
        sender = log.args['from']
        recipient = log.args.to
        amount = log.args.value
        block_number = log.blockNumber
        timestamp = web3_api.eth.get_block(block_number).timestamp
        date_time = datetime.fromtimestamp(timestamp)

        # Convert amount to human-readable format (assuming 6 decimals for USDC)
        amount_decimal = amount / 10**6

        print(f"Transfer at {date_time}: {sender} sent {amount_decimal} tokens to {recipient}")

        # Accumulate totals
        total_transfers += 1
        total_amount_sent += amount_decimal

        # Store details for further analysis
        transfer_details.append({
            "timestamp": date_time,
            "recipient": recipient,
            "amount": amount_decimal
        })

    # Print summary
    print("\nTransfer Summary:")
    print(f"Total transfers from {contract_address}: {total_transfers}")
    print(f"Total amount sent: {total_amount_sent} tokens")

    return transfer_details