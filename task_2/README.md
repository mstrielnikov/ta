# Task 2: Build Blockchain explorer (Python)

CLI application with the basic blockchain exploring functionality. It allows to perform:
* Got the kast blockchain's block: 
```bash
python main.py block-number
```
* Address balance lookup by executing:
```bash
python main.py balance 0x******
```

## Build
Dependencies:
* `web3`
* `python-dotenv`

## Exec
_Attention_. The `.env` file with the following content should be present in project's root to supply credentials during script startup:
```bash
WEB3_PROVIDER_URL="https://sepolia.infura.io/v3/************"
```

_Alternatively_, variable `WEB3_PROVIDER_URL` could be set as an environment variable:
```bash
export WEB3_PROVIDER_URL="https://sepolia.infura.io/v3/************"
```

There is two modes of execution (containerized & native):
* `native`. Execute the following sequence of commands in terminal (Linux or Mac):
    1. Build dependencies: `pip3 install -r requirements.txt`
    2. Run the CLI application with commands mentioned
* `containerized`. Executes the same sequence as above but within the short-living container to left your PC clean and avoid potential mismatch in dependency versions:
```bash
chmod +x run run_one_time_cntnr.sh
./run_one_time_cntnr.sh 0x****** # run demo script and exit. Please provide address to analyze as a script argument 
```

Example output:
```bash
Connected to Ethereum node successfully!
Latest block number: 7930998
Connected to Ethereum node successfully!
Balance of 0x******: 0.049856923187418002 ETH
```

# Explanation
The tool is built in top of `Web3.py` lib which provides interfaces for interacting with Ethereum nodes through Web3 provider. Infura provider was used in this example. 
The Web3 provider is a publically available HTTP Web endpoint (or multiple endpoints). Provider considered as a user friendly HTTP front-end and Etherum blockchain nodes are backend.
Blockchain nodes itself operating on top of RPC protocol. Only RPC queries are used on the level of nodes to query information from the blockchain as well for inter-node communication.
Web3 providers works as HTTP endpoints which serializes HTTP requests made with `Web3.py` to RPC to call blockchain node. That's enough in case if only user performs read-only query on the blochcain.
If we need to perform write operation to the blockchain, we should construct a transaction and sign it with our private key on behalf of wallet.

The blockchain explorer system works by connecting to an Ethereum node via the `Web3.py` library, querying the blockchain for data (block numbers, transactions, and balances), and presenting the information to the user in a readable format.

The tool wrap the functionality of `Web3.py` lib and provides CLI interface as a front-end for the end user.
The backend represented by `BlockchainExplorer` class. It initializes a connection to a public Ethereum node via HTTP Web3 provider.
Other providers are exposed by `Web3.py` (IPC and WebSockets), but HTTP is the easiest to go option since it widely supported.

Ethereum's distribute ledger orgonized in blocks. So in order to explore the recent activity on the blockchain we need to fetch the last block's address. The method `web3.eth.block_number` is used for thi purpose.
Then we can lookup the data from the latest block.

As for this example, we implemented `BlockchainExplorer.get_block_transactions()` method. 

The  method is used to takes a block number as input and calls `web3.eth.get_block(block_number, full_transactions=True)` to retrieve the full block data, including all transactions.
This functionality allows users to inspect the transactions included in a block, providing insights into recent network activity, such as payments, contract interactions etc.

Challenges Faced While Interacting with the Blockchain Network:
1. The code introduces additional layer of security to carefully manage credential with its explicit mention in the code. It's done by using env vars and read them in code. The production ready system should mask mention of credentials in logs as well. Ideally, credential management system should be set in order facilitate secure credential lifecycle on prod automatically. 
2. Access to the node via 3rd party APIs providers like Infura. This approach introduces limitations related node access by matching API rate limiter and facilitating Infura's credentials as well. The reliable network connection to the provider should be ensured and error-handled in the code.    
3. Data and unit formats. Ethereum stores values (balances and transaction amounts) in wei (the smallest fraction of ETH). Operation on Wei is difficult due to its size. The web3.from_wei utility was used to convert wei values to more readable units, such as ether (for balances and transaction values) and gwei (for gas prices). We used `web3.from_wei(balance_wei, 'ether')` to converts a balance from wei to ether for ease of use.
