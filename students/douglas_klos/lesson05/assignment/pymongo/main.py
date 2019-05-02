#!/usr/bin/env python3
""" Main functions to interface with MongoDB """

import argparse
from pprint import pprint
from loguru import logger
import src.database_operations as db


def main(argv=None):
    """Database main function
    """
    args = parse_cmd_arguments(argv)

    if args.disable_log:
        logger.disable("__main__")
        logger.disable("src.database_operations")

    if args.all_products:
        pprint(db.list_all_products())

    elif args.available_products:
        pprint(db.show_available_products())

    elif args.all_customers:
        pprint(db.list_all_customers())

    elif args.drop_collections:
        db.drop_databases()

    elif args.rentals_for_customer:
        pprint(db.rentals_for_customer(args.rentals_for_customer))

    elif args.customers_renting_product:
        pprint(db.show_rentals(args.customers_renting_product))

    elif args.insert:
        pprint(db.import_data(*args.insert))


def parse_cmd_arguments(args):
    """Parses the command line arguments

    Arguments:
        args {list} -- argument list from command line

    Returns:
        ArgumentParser.parse_args
    """
    parser = argparse.ArgumentParser(description="HPNorton Database Operations")
    parser.add_argument(
        "--all-products",
        help="Show list of all products",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--all-customers",
        help="Show list of all customers",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--available-products",
        help="Show list of available products",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--drop-collections",
        help="Drop customers, product, and rental collections",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--disable-log",
        help="Disable logging",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--rentals-for-customer",
        metavar="USER_ID",
        help="Show rentals for specified user_id",
        action="store",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--customers-renting-product",
        help="Show customers renting the specified product_id",
        metavar="PRODUCT_ID",
        action="store",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--insert",
        help="Loads csv files from specified data directory",
        metavar=("data_dir", "file1 file2"),
        action="store",
        required=False,
        default=False,
        nargs="*",
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    main()
