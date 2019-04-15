'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import traceback

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.NOTSET)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.NOTSET)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.NOTSET)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def parse_cmd_arguments():
    """
    method to parse through cmd line agrument
    """
    logging.info(
        'Start Debug: parse_cmd_arguments()')
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument(
        '-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument("-d", "--debug", help="debugger level", required=False)
    logging.info('End: parse_cmd_arguments() \n')
    return parser.parse_args()


def set_logging_level(debug_level):
    """
    sets the logging level
    """
    logging.info(
        'Start Debug: set_logging_level(debug_level)')

    if debug_level == "0":
        pass
    elif debug_level == "1":
        LOGGER.setLevel(logging.ERROR)
    elif debug_level == "2":
        LOGGER.setLevel(logging.WARNING)
    elif debug_level == "3":
        LOGGER.setLevel(logging.DEBUG)


    logging.info('End: set_logging_level(debug_level) \n')


def load_rentals_file(filename):
    """
    method to load rental file
    """


    logging.info('Start Debug: load_rentals_file(filename)')
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.warning("is %s the correct file?", repr(file.name))
        except Exception:
            logging.error('Fix the source.json @')
            logging.error(traceback.format_exc())  # used to see type of error
            exit(0)

    logging.info('End: load_rentals_file(filename) \n')
    return data


def calculate_additional_fields(data):
    """
    method to calculate additional fields
    """


    logging.info('Start: calculate_additional_fields(data)')
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')

        except ValueError as time_data_error:
            logging.error('%s', time_data_error)
            logging.debug(" value at  %s", value)

        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.error('Dates are switched')
            logging.debug("current start date %s", value['rental_start'])
            logging.debug("current end date %s", value['rental_end'])
            value["rental_start"] = value["rental_start"]
            value["rental_end"] = value["rental_end"]
            rental_start = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            logging.debug("this value has to be positive %s \n",
                          value['total_days'])
        else:
            value['total_days'] = (rental_end - rental_start).days

        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError as math_domain_error:
            logging.error('%s', math_domain_error)

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError:
            logging.debug(value['total_price'])
            logging.debug(value['units_rented'])
            logging.error('%s', ZeroDivisionError)
            logging.error("Calc = (total_price / units_rented  =  (%s / %s)",
                          value['total_days'], value['price_per_day'])
        else:
            pass


    logging.info('End: calculate_additional_fields(data) \n')

    return DATA


def save_to_json(filename, data):
    """
    method to save to json
    """
    logging.info(
        'Start: save_to_json(filename, data)')
    with open(filename, 'w') as file:
        try:
            json.dump(data, file)
            logging.warning("is %s the correct file?", repr(file.name))

        except Exception:
            logging.error(traceback.format_exc())  # used to see type of error
    logging.info('End: save_to_json(filename, data) \n')


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DEBUG_ARG = ARGS.debug
    set_logging_level(DEBUG_ARG)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
