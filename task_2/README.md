# Task # 2: Build Blochain explorer (Python)

# Functionality 
Smart contract (see `contracts/Election.sol`) follows the following logic:
* In order to simulate voting, smart contract performs transition between 3 states (election phases):
  1. 'ballot' during which candidates are being registered + prevention of candidate double registration
  2. 'ongoing' to accept votes + prevention from double voting
  3. 'submit' to submit votes and announce winner
* Each transition initiated by smart contract owner and emits a corresponded event (potentially to notify frontend) 
* Contract does not accept token payments in order to keep logic simple and not expose potential [reentrancy attacks](https://www.quicknode.com/guides/ethereum-development/smart-contracts/a-broad-overview-of-reentrancy-attacks-in-solidity-contracts)
* Additional methods `fallback` and `receive` implemented in order to prevent direct Eth transaction to contract's address  

Example of deployed smart contract:
[0xd32731dA1D5c7C7d47e12bd098b38d61bae9D0A2](https://sepolia.etherscan.io/address/0xd32731dA1D5c7C7d47e12bd098b38d61bae9D0A2)

# Build
_Attention_
The `.env` file with the following content should be present in path `scripts/.env` to supply credentials during script startup:
```bash
PRIVATE_KEY="************"
ACCOUNT_ADDRESS="0x******"
WEB3_PROVIDER_URL="https://sepolia.infura.io/v3/********"
```

There is two modes of execution (containerized & native):
* `native`. Execute the following sequence of commands in terminal (Linux or Mac):
* `containerized`. Executes the same sequence as above but within the short-living container to left your PC clean and avoid potential mismatch in dependency versions:
```bash
chmod +x run run_one_time_cntnr.sh
./run_one_time_cntnr.sh
```

Example output:
```bash
Connected to Ethereum node successfully!
Latest block number: 7930998
Connected to Ethereum node successfully!
Balance of 0x******: 0.049856923187418002 ETH
```


The blockchain explorer is a Python-based tool that interacts with the Ethereum blockchain to retrieve and display information such as block numbers, transactions, and account balances. Here's a step-by-step breakdown of its operation:

    Connection to the Ethereum Network:
        Component: The system uses the Web3.py library, a Python interface for interacting with Ethereum nodes.
        Process: The BlockchainExplorer class initializes a connection to a public Ethereum node via an HTTP provider. In this case, Infura is used as the node provider, which offers a free tier for accessing the Ethereum mainnet. The connection is established using the Web3.HTTPProvider class, and the is_connected() method verifies that the connection is successful.
        Purpose: This connection allows the system to send requests to the Ethereum blockchain and receive responses, enabling access to blockchain data without running a full Ethereum node locally.
    Querying the Latest Block Number:
        Component: The get_latest_block_number() method.
        Process: This method calls web3.eth.block_number, an API provided by Web3.py, which queries the Ethereum node for the most recent block number on the blockchain. The block number represents the height of the blockchain, i.e., the total number of blocks mined up to the current moment.
        Purpose: Knowing the latest block number is essential for exploring recent activity on the blockchain, such as fetching transactions from the latest block.
    Retrieving Transactions in a Block:
        Component: The get_block_transactions() method.
        Process: This method takes a block number as input and uses web3.eth.get_block(block_number, full_transactions=True) to retrieve the full block data, including all transactions. The full_transactions=True parameter ensures that complete transaction details (not just transaction hashes) are returned. The method then processes each transaction, extracting key details such as:
            Transaction hash
            Sender (from) and recipient (to) addresses
            Value transferred (converted from wei to ether using web3.from_wei)
            Gas and gas price (converted to appropriate units)
        Purpose: This functionality allows users to inspect the transactions included in a block, providing insights into recent network activity, such as payments, contract interactions, and more.
    Checking an Address Balance:
        Component: The get_address_balance() method.
        Process: This method takes an Ethereum address as input, ensures it is in the correct checksum format using web3.to_checksum_address(), and then queries the Ethereum node using web3.eth.get_balance() to retrieve the balance in wei. The balance is converted from wei to ether for user readability using web3.from_wei.
        Purpose: This allows users to check the ETH balance of any Ethereum address, which is useful for monitoring account activity or verifying funds.
    User Interface:
        Component: The main() function.
        Process: The script provides a simple menu-driven interface where users can select options to:
            Get the latest block number
            List transactions in the latest block
            Check the balance of an Ethereum address
            Exit the program
        The interface includes error handling and a small delay (time.sleep(1)) between requests to prevent overwhelming the node provider with too many requests in a short time (rate limiting).
        Purpose: This makes the tool user-friendly, allowing non-technical users to interact with the blockchain without needing to understand the underlying API calls.
    Error Handling:
        Component: Try-except blocks throughout the code.
        Process: Each method includes error handling to catch and report issues such as network errors, invalid addresses, or API failures. For example, if an invalid address is provided, the to_checksum_address method will raise an exception, which is caught and reported to the user.
        Purpose: This ensures the system is robust and provides meaningful feedback to users when something goes wrong.

Challenges Faced While Interacting with the Blockchain Network

Interacting with a public blockchain network, especially Ethereum, presents several challenges, particularly when using public nodes like Infura. Below are the key challenges faced during the development of this blockchain explorer, along with how they were addressed:

    Node Access and Rate Limiting:
        Challenge: Public Ethereum nodes, such as those provided by Infura, impose rate limits on API requests to prevent abuse. For example, Infura's free tier limits users to 100,000 requests per day, and there may be additional restrictions on requests per second. Exceeding these limits results in HTTP 429 (Too Many Requests) errors, causing the explorer to fail temporarily.
        Solution: A small delay (time.sleep(1)) was added between menu iterations to reduce the frequency of requests. For production use, more sophisticated solutions could include:
            Implementing request queuing or throttling logic
            Using a paid plan with higher rate limits
            Running a local Ethereum node to avoid external rate limits entirely
        Implication: This challenge highlights the trade-off between convenience (using a public node) and control (running a private node). For a simple explorer, the public node approach is sufficient, but for heavy usage, a private node might be necessary.
    Data Formatting and Unit Conversion:
        Challenge: Ethereum stores values (such as balances and transaction amounts) in wei, the smallest unit of ETH (1 ETH = 10^18 wei). Displaying these values in wei is not user-friendly, as the numbers are extremely large and difficult to interpret.
        Solution: The web3.from_wei utility was used to convert wei values to more readable units, such as ether (for balances and transaction values) and gwei (for gas prices). For example, web3.from_wei(balance_wei, 'ether') converts a balance from wei to ether.
        Implication: Proper unit conversion is critical for user experience, and care must be taken to use the correct units for different types of data (e.g., ether for value, gwei for gas prices).
    Error Handling and Network Reliability:
        Challenge: Interacting with a blockchain network involves network communication, which is inherently unreliable. Issues such as network timeouts, node outages, or invalid data can cause the explorer to fail. For example, an invalid Ethereum address (e.g., one with incorrect characters) will cause the get_balance call to fail.
        Solution: Comprehensive error handling was implemented using try-except blocks around all blockchain interactions. Specific errors, such as invalid addresses, are caught and reported to the user with meaningful messages. Additionally, the initial connection check (web3.is_connected()) ensures the explorer fails early if the node is unreachable.
        Implication: Robust error handling is essential for a production-ready system, as it prevents crashes and provides users with actionable feedback. For a more advanced system, additional error recovery mechanisms (e.g., retrying failed requests) could be implemented.
    Performance and Scalability:
        Challenge: Fetching block data, especially for blocks with many transactions, can be slow due to the volume of data involved. For example, a block might contain hundreds of transactions, each requiring significant processing to extract and format relevant information. This can lead to delays in the user interface, especially when using a public node with limited bandwidth.
        Solution: For this simple explorer, the performance issue was mitigated by focusing on the latest block only, which is typically cached by public nodes and thus faster to retrieve. For a more advanced system, potential solutions include:
            Caching frequently accessed data (e.g., recent blocks) locally
            Using a full archive node for faster access to historical data
            Implementing pagination for transaction lists to avoid processing too many transactions at once
        Implication: Performance is a significant concern for blockchain explorers, especially those intended for public use. The choice of node provider and caching strategy can greatly impact user experience.
    Security Considerations:
        Challenge: Using a public node involves security risks, such as exposing sensitive data (e.g., the Infura project ID) or being vulnerable to man-in-the-middle attacks if the connection is not secure. Additionally, user inputs (e.g., Ethereum addresses) must be validated to prevent injection attacks or other malicious behavior.
        Solution: The script includes a note to secure the Infura project ID (e.g., by using environment variables instead of hardcoding it). The web3.to_checksum_address method ensures that addresses are valid and properly formatted, reducing the risk of errors or attacks. For a production system, additional security measures could include:
            Using HTTPS for all node connections
            Implementing input sanitization beyond address validation
            Adding authentication for sensitive operations
        Implication: Security is a critical concern when dealing with blockchain data, as errors or vulnerabilities could lead to financial losses or data breaches. For a simple explorer, the current measures are sufficient, but a production system would require more rigorous security practices.
    Limited Node Capabilities:
        Challenge: Public nodes like Infura do not always provide full archive node capabilities, meaning some historical data or advanced queries (e.g., tracing internal transactions) may not be available. This limits the functionality of the explorer compared to what could be achieved with a full node.
        Solution: For this simple explorer, the focus was on basic functionality (latest block, transactions, and balances), which is well-supported by public nodes. For more advanced features, a full node or a specialized service (e.g., Etherscan API) would be required.
        Implication: The choice of node provider dictates the capabilities of the explorer. For educational or simple use cases, a public node is sufficient, but for comprehensive blockchain analysis, a full node or third-party API might be necessary.

Summary

The blockchain explorer system works by connecting to an Ethereum node via the Web3.py library, querying the blockchain for data (block numbers, transactions, and balances), and presenting the information to the user in a readable format. The system is designed to be user-friendly, with a simple menu interface and robust error handling.

However, interacting with the blockchain network presents several challenges, including rate limiting, data formatting, network reliability, performance, security, and node capabilities. These challenges were addressed through careful design choices, such as using delays to prevent rate limiting, converting units for readability, implementing error handling, and focusing on basic functionality supported by public nodes. For a production-ready system, additional enhancements (e.g., caching, advanced error recovery, and security measures) would be necessary to overcome these challenges more comprehensively.