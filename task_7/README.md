# Task 7: Python Script For Smart Contract Data Parsing

Python script to track source/destination of transfer made from/to contract address (given from Task #1):

## Build
Dependencies:
* `web3`
* `python-dotenv`

## Exec
_Attention_. The `.env` file with the following content should be present in project's root to supply credentials during script startup:
```bash
WEB3_PROVIDER_URL = "https://sepolia.infura.io/v3/********"
SOURCE_CONTRACT_ADDRESS = "0x***************"
TARGET_ADDRESS = "0x*******************"
```

_Alternatively_, variable `WEB3_PROVIDER_URL` could be set as an environment variable:
```bash
export WEB3_PROVIDER_URL="https://sepolia.infura.io/v3/************"
```

There is two modes of execution (containerized & native):
* `native`. Execute the following sequence of commands in terminal (Linux or Mac):
    1. Build dependencies: `pip3 install -r requirements.txt`
    2. To run the script execute `python3 main.py` 
* `containerized`. Executes the same sequence as above but within the short-living container to left your PC clean and avoid potential mismatch in dependency versions:
```bash
chmod +x run run_one_time_cntnr.sh
./run_one_time_cntnr.sh # run demo script and exit
```

Example output:
```bash
Analyzing token transfers from block 7957876 to 7958876...

Transfer Summary:
Total transfers from 0x263596609160D18e726ecBBb5E7fB03a4F01932C: 0
Total amount sent: 0 tokens
```
We can see that no transfers was made by certain wallet. That's because the design of the smart contract from task #1 prevents transfer of funds to keep implementation light.  

## Explanations
The parsing of transaction date was made through wrapping of `web3.py` functionality. In order to request the data, we need to perform RPC-query to the node. Since we are working through HTTP lib, we added a payload with the content of query which will be executed on node after request deserialization and following  serilization of RPC payload in binary RPC-compatible format.
We put the RPC-payload in a separate file `./rpc_transfers.json` to avoid its hard coding. In case of script functionality change, we can introduce new query in different `.json` file.
