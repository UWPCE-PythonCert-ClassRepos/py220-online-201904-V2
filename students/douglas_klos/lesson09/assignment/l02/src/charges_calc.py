#!/usr/bin/env python3
"""Returns total price paid for individual rentals"""

# Douglas Klos
# April 9th, 2019
# Python 220
# Lesson 02, debugging and logger

import sys
import argparse
import json
from datetime import datetime as dt
from math import sqrt
from loguru import logger

LOG_FILE = dt.now().strftime("%Y-%m-%d") + ".log"
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"


def main():
    """main function"""

    logger.remove()
    logger.add(LOG_FILE, level="DEBUG")
    logger.add(sys.stderr, level="DEBUG")

    args = parse_cmd_arguments()
    set_debug_level(args)
    data = load_rentals_file(args.input)
    data = repair_dates(data)
    data, bad_data = calculate_additional_fields(data)
    data = remove_bad_data(data, bad_data)
    save_to_json(args.output, data)
    save_to_json(args.output + ".bad", bad_data)


def parse_cmd_arguments():
    """Parses the command line arguments

    Returns:
        ArgumentParser.parse_args

    """
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("-i", "--input", help="input JSON file", required=True)
    parser.add_argument("-o", "--output", help="ouput JSON file", required=True)
    parser.add_argument("-d", "--debug", help="debugger level", required=False)
    return parser.parse_args()


def set_debug_level(args):
    """Sets the debug level based on command line arguments"""

    if args.debug:
        if args.debug == "0":
            logger.disable("__main__")
        elif args.debug == "1":
            logger.remove()
            logger.add(LOG_FILE, level="DEBUG")
            logger.add(sys.stderr, level="DEBUG")
        elif args.debug == "2":
            logger.remove()
            logger.add(LOG_FILE, level="INFO")
            logger.add(sys.stderr, level="INFO")
        elif args.debug == "3":
            logger.remove()
            logger.add(LOG_FILE, level="WARNING")
            logger.add(sys.stderr, level="WARNING")
        elif args.debug == "4":
            logger.remove()
            logger.add(LOG_FILE, level="ERROR")
            logger.add(sys.stderr, level="ERROR")
        else:
            print(f"Invalid debug level specified: {args.debug}.  (0-4)")
            exit(0)


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
            new_data = json.load(file)
        except json.decoder.JSONDecodeError as ex:
            logger.critical(
                "Loading data from json failed."
                "\n\tThe following error should contain the line where the "
                "problem occured.\n\tFix the source file and try again."
                "\n\tException: %s", repr(ex)
            )
            exit(0)
    return new_data


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


def save_to_json(filename, data):
    """Saves the input_data to filename in json format

    Args:
        input_data (dict): Dictionary of data to be saved

    """
    logger.info(f"-----Start of save_to_json({filename}, data)-----")
    with open(filename, "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
