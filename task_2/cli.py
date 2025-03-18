import argparse


def setup_argparse():
    parser = argparse.ArgumentParser(
        description="Ethereum Blockchain Explorer",
        usage="%(prog)s [options]"
    )

    # # Required provider URL argument
    # parser.add_argument(
    #     "--endpoint",
    #     required=True,
    #     help="ETH API node endpoint URL"
    # )

    # Subcommands for different operations
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Block number command
    subparsers.add_parser(
        "block-number",
        help="Get the latest block number"
    )

    # Block transactions command
    tx_parser = subparsers.add_parser(
        "block-transactions",
        help="Get transactions in a specific block"
    )
    tx_parser.add_argument(
        "--block",
        type=int,
        help="Specific block number (defaults to latest if not provided)"
    )

    # Address balance command
    balance_parser = subparsers.add_parser(
        "balance",
        help="Get the balance of an Ethereum address"
    )
    balance_parser.add_argument(
        "address",
        help="Ethereum address to check balance for"
    )

    return parser