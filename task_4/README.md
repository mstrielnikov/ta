# Ethereum Backend Service

Golang backend service to view the Ethereum blockchain endpoints via `go-ethereum` library.

It provides an HTTP API to fetch the latest block and the balance of a given Ethereum address, specifically designed to work with the Sepolia testnet (but can be configured for other networks).

## Dependencies
* `go-ethereum`
* 

## Build 



## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Go**: Version 1.18 or later. Download and install from [the official Go website](https://golang.org/dl/).
- **Git**: For cloning the repository (optional if you manually download the code).
- **curl** or **Postman**: For testing the API endpoints.
- **Infura Account**: An account with Infura (or another Ethereum node provider) to access the Sepolia testnet. Sign up at [Infura](https://infura.io/).

## Features

- Connects to an Ethereum node (e.g., Sepolia testnet via Infura).
- Fetches the latest block on the blockchain.
- Fetches the balance of a specified Ethereum address.
- Exposes data via a simple HTTP API.
- Includes structured debug logging using `logrus`.

## Setup

### Step 1: Clone the Repository

If you have Git installed, clone the repository to your local machine:

```bash
git clone <repository-url>
cd eth-backend-service