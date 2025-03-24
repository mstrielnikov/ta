import argparse


def setup_argparse():
    parser = argparse.ArgumentParser(
        description="Ethereum Blockchain Explorer",
        usage="%(prog)s [options]"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser(
        "block-number",
        help="Get the latest block number"
    )

    tx_parser = subparsers.add_parser(
        "block-transactions",
        help="Get transactions in a specific block"
    )
    tx_parser.add_argument(
        "--block",
        type=int,
        help="Specific block number (defaults to latest if not provided)"
    )

    balance_parser = subparsers.add_parser(
        "balance",
        help="Get the balance of an Ethereum address"
    )
    balance_parser.add_argument(
        "address",
        help="Ethereum address to check balance for"
    )

    return parser