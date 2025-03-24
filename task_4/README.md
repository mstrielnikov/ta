# Task 4: Build Blockchain explorer (Golang)

Golang backend service to view the Ethereum blockchain endpoints via `go-ethereum` library.
It provides an HTTP API to fetch the latest block and the balance of a given Ethereum address.

The service exposes such REST API endpoints (on port with 8080 as default):
* `GET` `/block/latest` to get a hash of the latest block 
* `GET` `/balance/0x*********` to to lookup balance by wallet address

## Dependencies
* `github.com/joho/godotenv`
* `github.com/ethereum/go-ethereum/common`
* `github.com/ethereum/go-ethereum/ethclient`
* `github.com/julienschmidt/httprouter`

## Build
_Attention_. The `.env` file with the following content should be present in project's root to supply credentials during script startup:
```bash
ETH_NODE_URL="https://sepolia.infura.io/v3/***********"
PORT="8080"
```

_Alternatively_, variable `ETH_NODE_URL` could be set as an environment variable:
```bash
export ETH_NODE_URL="https://sepolia.infura.io/v3/************"
export PORT="8080"
```

## Launch
There is two modes of execution (containerized & native):
* `native`. Execute the following sequence of commands in terminal (Linux or Mac):
    1. Build dependencies in the root of the project: `go build && go run`
    2. The service is ready to accept REST API GET requests mentioned above  
* `containerized`. Executes the same sequence as above but within the short-living container to left your PC clean and avoid potential mismatch in dependency versions:
```bash
chmod +x run run_one_time_cntnr.sh
./run_one_time_cntnr.sh # run demo script and exit
```

Example output:
```bash
Connected to Ethereum node successfully!
Latest block number: 7930998
Connected to Ethereum node successfully!
Balance of 0x******: 0.049856923187418002 ETH
```

# Explanation

The architecture is a very similar to the python's version from [Task 2](../task_2/README.md). But it's built on top of analogous Go lang's stack and CLI interface replaced by HTTP API as a user front-end.
The service exposes HTTP endpoints to lookup data from blockchain. The `github.com/julienschmidt/httprouter` used as HTTP handler. It allows easily introduce any new HTTP handler and associate corresponding function with handling.
The following considerations implied the choice of this lib:
* HTTP variables are supported to make it easier to scale with growing functionality or parametraized HTTP requests
* It's lightweight and has low memory footprint trough implementation of zero-allocation strategy
* It's well maintained lib used across numerous projects like `fiber` framework. So `fiber` framework may be introduced in the future at a low cost to provide full-fledged backend development capabilities and decent docs aside
* Standard logging lib was used in order to keep executable small and introduce no dependencies then needed. Standard logging lib may be replaced in the future.

Credentials are managed at the same way as in [Task 2](../task_2/README.md) via `.env` files to supply env vars and not hard code them explicitly.