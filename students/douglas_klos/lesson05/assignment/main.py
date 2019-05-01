#!/usr/bin/env python3
# pylint: disable=E0401
""" Main functions to interface with MongoDB """

import argparse
from pprint import pprint
from loguru import logger
import src.database_operations as db


def main(argv=None):
    """Database main function
    """
    args = parse_cmd_arguments(argv)

    if args.log:
        logger.disable("__main__")
        logger.disable("src.database_operations")

    if args.drop:
        db.drop_databases()

    if args.rental:
        pprint(db.show_rentals(args.rental))

    if args.insert:
        pprint(db.import_data(*args.insert))

    if args.product:
        pprint(db.show_available_products())


def parse_cmd_arguments(args):
    """Parses the command line arguments

    Arguments:
        args {list} -- argument list from command line

    Returns:
        ArgumentParser.parse_args
    """
    parser = argparse.ArgumentParser(description="HPNorton Database Operations")
    parser.add_argument(
        "-d",
        "--drop",
        help="Drop customers, product, and rental collections",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-p",
        "--product",
        help="Show list of available products",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-l",
        "--log",
        help="Disable logging",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-i",
        "--insert",
        help="datadir file1 file2 file3",
        action="store",
        required=False,
        default=False,
        nargs="*",
    )
    parser.add_argument(
        "-r",
        "--rental",
        help="Show rentals for specified product_id",
        action="store",
        required=False,
        default=False,
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    main()
