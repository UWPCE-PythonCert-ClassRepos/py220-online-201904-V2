#!/usr/bin/env python3
"""Returns total price paid for individual rentals"""


from sys import argv, stderr
from argparse import ArgumentParser
from json import load, decoder, dump
from datetime import datetime as dt
from math import sqrt
from loguru import logger


def disable_logging(func):
    """ Decorator to disable logging in functions """
    def logged(*args, **kwargs):
        if "-d" in argv:
            logger.disable("__main__")
        result = func(*args, **kwargs)
        logger.enable("__main__")
        return result
    return logged


@disable_logging
def parse_cmd_arguments():
    """Parses the command line arguments

    Returns:
        ArgumentParser.parse_args

    """
    parser = ArgumentParser(description="Process some integers.")
    parser.add_argument("-i", "--input", help="input JSON file", required=True)
    parser.add_argument("-o", "--output", help="ouput JSON file", required=True)
    parser.add_argument(
        "-d",
        "--disable",
        help="disable_logging",
        action="store_true",
        required=False,
    )
    return parser.parse_args()


@disable_logging
def load_rentals_file(filename):
    """Loads rental data from input json file

    Args:
        filename: Filename to read data from

    Returns:
        dict: Dictionary of rental data

    """
    logger.info("-----Start of load_rental_file-----")
    with open(filename) as file:
        try:
            new_data = load(file)
        except decoder.JSONDecodeError as ex:
            logger.critical(
                "Loading data from json failed."
                "\n\tThe following error should contain the line where the "
                "problem occured.\n\tFix the source file and try again."
                "\n\tException: %s",
                repr(ex),
            )
            exit(0)
    return new_data


@disable_logging
def repair_dates(data):
    """Repairs incorrect dates in data

    Args:
        input_data (dict): Dictionary of data to be parsed

    Returns:
        dict: Dictionary with dates repaired

    """
    logger.info("-----Start of repair_dates-----")
    for key, value in data.items():
        try:
            rental_start = dt.strptime(value["rental_start"], "%m/%d/%y")
            rental_end = dt.strptime(value["rental_end"], "%m/%d/%y")
            if rental_end < rental_start:
                logger.warning(
                    f"Key:{key} rental start, end dates reversed.  Repairing"
                )
                value["rental_start"], value["rental_end"] = (
                    value["rental_end"],
                    value["rental_start"],
                )
        except ValueError:
            logger.error(f"Key:{key} contains bad date data.  Skipping.")
            logger.debug(f"Value:{value}")
    return data


@disable_logging
def calculate_additional_fields(data):
    """Calculates additional fields of data

    Args:
        input_data (dict): Dictionary of data to be parsed

    Returns:
        dict, dict: good_data, bad_data

    """
    bad_data = {}
    logger.info("-----Start of load_additional_fields-----")
    for key, value in data.items():
        try:
            rental_start = dt.strptime(value["rental_start"], "%m/%d/%y")
            rental_end = dt.strptime(value["rental_end"], "%m/%d/%y")
            value["total_days"] = (rental_end - rental_start).days
            value["total_price"] = value["total_days"] * value["price_per_day"]
            value["sqrt_total_price"] = sqrt(value["total_price"])
            value["unit_cost"] = value["total_price"] / value["units_rented"]
        except (ZeroDivisionError, ValueError):
            bad_data[key] = value
            logger.error(
                f"Key:{key} Failed calculating additional fields.  Skipping."
            )
            logger.debug(f"Value:{value}")
    return data, bad_data


@disable_logging
def remove_bad_data(data, bad_data):
    """Removes bad entries from the dictionary

    Args:
        input_data (dict): Dictionary of data to be parsed
        input_bad_data (dict): Dictionary of bad json entries to be removed

    Returns:
        dict: Dictionary of valid entries

    """
    for key in bad_data:
        del data[key]
    return data


@disable_logging
def save_to_json(filename, data):
    """Saves the input_data to filename in json format

    Args:
        input_data (dict): Dictionary of data to be saved

    """
    logger.info(f"-----Start of save_to_json({filename}, data)-----")
    with open(filename, "w") as file:
        dump(data, file)


def main():
    """main function"""

    log_file = dt.now().strftime("%Y-%m-%d") + ".log"

    logger.remove()
    logger.add(log_file, level="DEBUG")
    logger.add(stderr, level="DEBUG")

    args = parse_cmd_arguments()

    data, bad_data = calculate_additional_fields(
        repair_dates(load_rentals_file(args.input))
    )
    save_to_json(args.output, remove_bad_data(data, bad_data))
    save_to_json(args.output + ".bad", bad_data)


if __name__ == "__main__":
    main()
