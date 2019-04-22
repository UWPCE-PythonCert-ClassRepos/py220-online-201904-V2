""" Returns total price paid for individual rentals """
import argparse
import json
import datetime
import math
import sys
from loguru import logger

FORMATTER = "{time:YYYY-MM-DD HH:mm:ss.SSS} {file}:{line} {level} {message}"  # formatter for logger
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"  # logger file name


def main():
    """ main activity of code"""
    args = parse_cmd_arguments()
    console_level, log_file_level = set_the_level(args.debug)
    if console_level:
        console_handler = dict(sink=sys.stderr, format=FORMATTER, level=console_level)
        file_handler = dict(sink=LOG_FILE, format=FORMATTER, backtrace=True, level=log_file_level)
        logger.configure(handlers=[console_handler, file_handler])
    data = load_rentals_file(args.input)
    new_data = calculate_additional_fields(data)
    save_to_json(args.output, new_data)


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
    if debug_choice == 0:
        logger.remove()
        logger.disable(__name__)
        con_level, file_level = None, None
    elif debug_choice == 1:
        logger.remove()
        con_level, file_level = "ERROR", "ERROR"
    elif debug_choice == 2:
        logger.remove()
        con_level, file_level = "WARNING", "WARNING"
    elif debug_choice == 3:
        logger.remove()
        con_level, file_level = "DEBUG", "WARNING"
    return con_level, file_level


def load_rentals_file(filename):
    """ Open the json file and load the data in data variable"""
    with open(filename) as file:
        try:
            load_data = json.load(file)
        except json.decoder.JSONDecodeError:
            logger.exception("json file is corrupted, decoder is failed")
            exit(0)
    return load_data


def calculate_additional_fields(load_data):
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


if __name__ == "__main__":
    main()
