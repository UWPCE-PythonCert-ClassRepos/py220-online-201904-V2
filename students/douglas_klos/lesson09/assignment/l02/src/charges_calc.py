#!/usr/bin/env python3
"""Returns total price paid for individual rentals"""

# Douglas Klos
# April 9th, 2019
# Python 220
# Lesson 02, debugging and logging

import argparse
import json
import datetime
import math
import logging


LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLER_HANDLER = logging.StreamHandler()
CONSOLER_HANDLER.setLevel(logging.DEBUG)
CONSOLER_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.NOTSET)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLER_HANDLER)

LOGGER.disabled = True


def main():
    """main function"""
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
    logging.info("Start of parse_cmd_arguments()")  # We'll never see this
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("-i", "--input", help="input JSON file", required=True)
    parser.add_argument("-o", "--output", help="ouput JSON file", required=True)
    parser.add_argument("-d", "--debug", help="debugger level", required=False)
    return parser.parse_args()


def set_debug_level(args):
    """Sets the debug level based on command line arguments"""
    if args.debug:
        if args.debug == "0":
            pass
        elif args.debug == "1":
            LOGGER.disabled = False
            LOGGER.setLevel(logging.ERROR)
        elif args.debug == "2":
            LOGGER.disabled = False
            LOGGER.setLevel(logging.WARNING)
        elif args.debug == "3":
            LOGGER.disabled = False
            LOGGER.setLevel(logging.DEBUG)
        else:
            print(f"Invalid debug level specified: {args.debug}.  (0-3)")
            exit(0)


def load_rentals_file(filename):
    """Loads rental data from input json file

    Args:
        filename: Filename to read data from

    Returns:
        dict: Dictionary of rental data

    """
    logging.info("-----Start of load_rental_file-----")
    with open(filename) as file:
        try:
            new_data = json.load(file)
        except json.decoder.JSONDecodeError as ex:
            logging.critical(
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
    logging.info("-----Start of repair_dates-----")
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(
                value["rental_start"], "%m/%d/%y"
            )
            rental_end = datetime.datetime.strptime(
                value["rental_end"], "%m/%d/%y"
            )
            if rental_end < rental_start:
                logging.warning(
                    "Key:%s rental start, end dates reversed.  Repairing.", key
                )
                value["rental_start"], value["rental_end"] = (
                    value["rental_end"],
                    value["rental_start"],
                )
        except ValueError:
            logging.error("Key:%s contains bad date data.  Skipping.", key)
            logging.debug("Value:%s", value)
    return data


def calculate_additional_fields(data):
    """Calculates additional fields of data

    Args:
        input_data (dict): Dictionary of data to be parsed

    Returns:
        dict, dict: good_data, bad_data

    """
    bad_data = {}
    logging.info("-----Start of load_additional_fields-----")
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(
                value["rental_start"], "%m/%d/%y"
            )
            rental_end = datetime.datetime.strptime(
                value["rental_end"], "%m/%d/%y"
            )
            value["total_days"] = (rental_end - rental_start).days
            value["total_price"] = value["total_days"] * value["price_per_day"]
            value["sqrt_total_price"] = math.sqrt(value["total_price"])
            value["unit_cost"] = value["total_price"] / value["units_rented"]
        except (ZeroDivisionError, ValueError):
            bad_data[key] = value
            logging.error(
                "Key:%s Failed calculating additional fields.  Skipping.", key
            )
            logging.debug("Value:%s", value)
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
    logging.info("-----Start of save_to_json(%s, data)-----", filename)
    with open(filename, "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()
