from web3 import Web3

class BlockchainExplorer:
    def __init__(self, web3_provider: Web3):
        self.web3 = web3_provider

    def get_latest_block_number(self):
        try:
            block_number = self.web3.eth.block_number
            return block_number
        except Exception as e:
            print(f"Error getting latest block number: {e}")
            return None

    def get_block_transactions(self, block_number):
        try:
            block = self.web3.eth.get_block(block_number, full_transactions=True)

            transactions = []
            for tx in block['transactions']:
                transaction_info = {
                    'hash': tx['hash'].hex(),
                    'from': tx['from'],
                    'to': tx['to'],
                    'value': self.web3.from_wei(tx['value'], 'ether'),
                    'gas': tx['gas'],
                    'gas_price': self.web3.from_wei(tx['gasPrice'], 'gwei')
                }
                transactions.append(transaction_info)
            return transactions
        except Exception as e:
            print(f"Error getting block transactions: {e}")
            return None

    def get_address_balance(self, address):
        try:
            # Ensure address is checksummed
            checksum_address = self.web3.to_checksum_address(address)
            balance_wei = self.web3.eth.get_balance(checksum_address)
            balance_eth = self.web3.from_wei(balance_wei, 'ether')
            return balance_eth
        except Exception as e:
            print(f"Error getting address balance: {e}")
            return None
