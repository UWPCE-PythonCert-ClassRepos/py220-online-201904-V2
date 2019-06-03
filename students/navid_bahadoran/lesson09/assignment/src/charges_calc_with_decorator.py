""" Returns total price paid for individual rentals """
import argparse
import json
import datetime
import math
import logging
from functools import wraps



def parse_cmd_arguments():
    """ create the argument for CLI
        -i or --input for input json file name
        -o or --output for output json file name
        -d or --debug to set which level of logging we need for our program
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='set the logger', required=True, type=int,
                        choices=[0, 1, 2, 3])

    return parser.parse_args()


def set_the_level(debug_choice):
    """ Set the level of logger
        0: No debug messages or log file.
        1: Only error messages.
        2: Error messages and warnings.
        3: Error messages, warnings and debug messages.
    """
    log_format = "%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s"  # formatter
    log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"  # logger file name

    def add_level(func):
        wraps(func)

        def wrapper():
            logger_handler = func()
            formatter = logging.Formatter(log_format)
            logger_handler.setLevel(logging.DEBUG)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger_handler.addHandler(console_handler)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger_handler.addHandler(file_handler)
            if debug_choice == 0:
                # logging.shutdown()
                logging.disable(logging.CRITICAL)
                logger_handler.removeHandler(file_handler)
                logger_handler.removeHandler(console_handler)
            elif debug_choice == 1:
                console_handler.setLevel(logging.ERROR)
                file_handler.setLevel(logging.ERROR)
            elif debug_choice == 2:
                console_handler.setLevel(logging.WARNING)
                file_handler.setLevel(logging.WARNING)
            elif debug_choice == 3:
                console_handler.setLevel(logging.DEBUG)
                file_handler.setLevel(logging.WARNING)
            return logger_handler

        return wrapper

    return add_level


def load_rentals_file(filename, logger):
    """ Open the json file and load the data in data variable"""
    with open(filename) as file:
        try:
            load_data = json.load(file)
        except json.decoder.JSONDecodeError:
            logger.exception("json file is corrupted, decoder is failed")
            exit(0)
    return load_data


def calculate_additional_fields(load_data, logger):
    """ calculate additional data from json file"""
    corrected_data = load_data.copy()
    for key, value in load_data.items():
        try:
            try:
                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            except ValueError:
                logger.warning(f"the date format of {key} was wrong. remove this data.")
                del corrected_data[key]
                continue
            if rental_end < rental_start:
                logger.warning(f"the end date and start date of {key}"
                               f" was reversed, and it is fixed.")
                logger.debug(f"The rental start date: {rental_start}")
                logger.debug(f"the rental end date: {rental_end}")
                value['rental_start'], value['rental_end'] = \
                    value['rental_end'], value['rental_start']
                rental_start, rental_end = rental_end, rental_start
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            try:
                value['unit_cost'] = value['total_price'] / value['units_rented']
            except ZeroDivisionError:
                logger.warning(f"unit_rented of {key} was zero, "
                               f"cause zero division. remove this data.")
                del corrected_data[key]
                continue

        except (ValueError, ZeroDivisionError):
            logger.exception("Error happened")
            logger.debug(f"bad data is:{key}")
            exit(0)

    return corrected_data


def save_to_json(filename, processed_data):
    """ saved the processed data in output file"""
    with open(filename, 'w') as file:
        json.dump(processed_data, file, indent=2)


ARGS = parse_cmd_arguments()


@set_the_level(ARGS.debug)
def start_logging():
    """ make a logger for logging activity"""
    return logging.getLogger(__name__)


LOGGER = start_logging()
DATA = load_rentals_file(ARGS.input, LOGGER)
NEW_DATA = calculate_additional_fields(DATA, LOGGER)
save_to_json(ARGS.output, NEW_DATA)
