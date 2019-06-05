#!/usr/bin/env python3
""" Main functions to interface with MongoDB """

import sys
from argparse import ArgumentParser
from pprint import pprint
from loguru import logger
import src.database_operations as db


def main(argv=None):
    """ Database main function """
    args = parse_cmd_arguments(argv)

    func_struct = (
        (args.disable_log, disable_log, ()),
        (args.all_products, db.list_all_products, ()),
        (args.available_products, db.show_available_products, ()),
        (args.all_customers, db.list_all_customers, ()),
        (args.all_rentals, db.list_all_rentals, ()),
        (args.drop_collections, db.drop_collections, ()),
        (args.drop_database, db.drop_database, ()),
        (
            args.rentals_for_customer,
            db.rentals_for_customer,
            (args.rentals_for_customer,),
        ),
        (
            args.customers_renting_product,
            db.customers_renting_product,
            (args.customers_renting_product,),
        ),
        (args.parallel, db.parallel, (args.parallel,)),
        (args.linear, db.linear, (args.linear,)),
    )

    pprint(
        list(
            map(
                lambda x: x[1](*x[2]),
                filter(lambda x: x[0] is not False, func_struct),
            )
        )[0]
    )


def disable_log():
    """ Disables logging for the system """
    logger.disable("__main__")
    logger.disable("src.database_operations")


def parse_cmd_arguments(args):
    """ Parses the command line arguments

    Arguments:
        args {list} -- argument list from command line

    Returns:
        ArgumentParser.parse_args
    """
    parser = ArgumentParser(description="HPNorton Database Operations")
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
        "--all-rentals",
        help="Show list of all rentals",
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
        "--drop-database",
        help="Drop database",
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
        "--parallel",
        help="Loads csv files from specified data directory",
        metavar=("--parallel", "file1 file2 file3 ..."),
        action="store",
        required=False,
        default=False,
        nargs="*",
    )
    parser.add_argument(
        "--linear",
        help="Loads csv files from specified data directory",
        metavar=("--linear", "file1 file2 file3 ..."),
        action="store",
        required=False,
        default=False,
        nargs="*",
    )
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args(args)


if __name__ == "__main__":
    main()
