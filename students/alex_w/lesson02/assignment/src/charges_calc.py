
'''
Returns total price paid for individual rentals
'''


import argparse
import json
import datetime
import math
from loguru import logger

logger.start("charges_calc.log", rotation="500 MB")


def parse_cmd_arguments():
    """
    Returns arguments as parsed.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='enable debugging',
                        default=0, required=False)
    return parser.parse_args()


def load_rentals_file(filename):
    """
    Exits with a FileNotFoundError.
    """
    with open(filename) as file:
        try:
            # pdb.set_trace()
            rentals = json.load(file)
        except FileNotFoundError:
            logger.error('Loading input file failed: File not found. Exiting.')
            exit(0)
        except json.JSONDecodeError:
            logger.warning('All data not loaded. JSON formatting error.')
    return rentals


def calculate_additional_fields(rental_data):
    """
        Calculates total days of rental, total price, and unit cost.

        """
    for value in rental_data.values():
        try:
            # pdb.set_trace()
            rental_start = datetime.datetime.strptime(
                value['rental_start'],
                '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_end'],
                '%m/%d/%y')
        except ValueError:
            logger.warning('Some data not decoded. Could not decode date.')
        try:
            value['total_days'] = (rental_end - rental_start).days
        except ValueError:
            logger.warning('Could not calculate total rental days due '
                           'to invalid start or end dates.')
        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
        except ValueError:
            logger.warning('Could not calculate price per day.')
        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
        except ValueError:
            logger.warning('Some data not decoded. Could not get square '
                           'root price due to invalid total price.')
        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            logger.warning('Some data not decoded. Could not get unit '
                           'cost due to invalid # units rented.')
    return rental_data


def save_to_json(filename, rental_data):
    """
    Saves rental data as JSON file name.
    """
    with open(filename, 'w') as file:
        json.dump(rental_data, file)


def set_logging_level(arg_level):
    """
    Sets logging levels
    """
    if arg_level == 3:
        return 'DEBUG'
    elif arg_level == 2:
        return 'WARNING'
    elif arg_level == 1:
        return 'ERROR'
    elif arg_level == 0:
        return 0
    else:
        raise ValueError('Please enter a number 0-3.')
        logger.error('Logging level out of range.')

if __name__ == "__main__":
    __args__ = parse_cmd_arguments()
    # Set up the logger
    if int(__args__.debug) > 0:
        logger.add(
            '{time:YYYY-MM-DD}.log',
            format='{time} {file}: {line} {message}',
            level=set_logging_level(int(__args__.debug))
            )
            # “%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s”
    logger.debug('Loading input file...')
    __data__ = load_rentals_file(__args__.input)
    logger.debug('Calculating data...')
    __data__ = calculate_additional_fields(__data__)
    logger.debug('Saving data...')
    save_to_json(__args__.output, __data__)
