from web3 import Web3
from solcx import compile_standard


def read_file(filepath):
    with open(filepath) as f:
        return f.read()

def solcx_compile(content, sol_version):
    try:
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"Election.sol": {"content": content}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                        }
                    }
                },
            },
            solc_version=sol_version,
        )
        return compiled_sol
    except Exception as e:
        raise f"Compilation failed: {e}"


def deploy_contract_tx(w3, account, private_key, abi, bytecode):
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.constructor().build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gasPrice': w3.eth.gas_price,
        'chainId': w3.eth.chain_id
    })

    # Sign and send the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction hash: {w3.to_hex(tx_hash)}")

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    print(f"Contract deployed at address: {contract_address}")

    return contract_address