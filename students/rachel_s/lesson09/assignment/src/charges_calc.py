#!/usr/bin/env python3

'''
Returns total price paid for individual rentals, now with fancy
decorator-based logging.
'''

# Rachel Schirra
# June 2, 2019
# Python 220 Lesson 02


import argparse
import json
import datetime
import math
from loguru import logger


def log_wrapper(func):
    '''
    A decorator that enables logging before and after a function is
    executed.
    '''
    def logged(*args, **kwargs):
        if args and kwargs:
            logger.debug('Executing {function} with args {args}'
                         'and kwargs {kwargs}'.format(
                             function=func.__name__, args=args, kwargs=kwargs))
        elif args:
            logger.debug('Executing {function} with args {args}'.format(
                function=func.__name__, args=args))
        elif kwargs:
            logger.debug('Executing {function} with args {kwargs}'.format(
                function=func.__name__, kwargs=kwargs))
        else:
            logger.debug('Executing {function} with no arguments'.format(
                function=func.__name__
            ))
        try:
            result = func(*args, **kwargs)
        except(
                FileNotFoundError,
                json.JSONDecodeError,
                ValueError
        ) as err:
            logger.warning(err)
        if result:
            logger.debug('Function {function} output: {result}'.format(
                function=func.__name__, result=result
            ))
        return result
    return logged


def parse_cmd_arguments():
    """
    Takes command arguments and returns arguments as parsed according to
    the JSON file
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='enable debugging',
                        default=0, required=False)
    return parser.parse_args()


def load_rentals_file(filename):
    """
    Loads rentals JSON file and exits with a FileNotFoundError if it
    encounters a problem.
    """
    with open(filename) as file:
        # pdb.set_trace()
        rentals = json.load(file)
    return rentals


def calculate_additional_fields(rental_data):
    """
    Accepts a rental_data JSON file.
    Calculates total days of rental, total price, and unit cost. Exits
    if a key is not found in rental_data.
    """
    for value in rental_data.values():
        rental_start = datetime.datetime.strptime(
            value['rental_start'],
            '%m/%d/%y')
        rental_end = datetime.datetime.strptime(
            value['rental_end'],
            '%m/%d/%y')
        value['total_days'] = (rental_end - rental_start).days
        value['total_price'] = value['total_days'] * value['price_per_day']
        value['sqrt_total_price'] = math.sqrt(value['total_price'])
        value['unit_cost'] = value['total_price'] / value['units_rented']
    return rental_data


def save_to_json(filename, rental_data):
    """
    Saves modified rental data as JSON with the specified file name.
    """
    with open(filename, 'w') as file:
        json.dump(rental_data, file)


def set_logging_level(arg_level):
    """
    Sets logging level based on level passed in command line args
    """
    if arg_level == 1:
        return 1
    elif arg_level == 0:
        return 0
    else:
        raise ValueError('Please enter 0 or 1.')

if __name__ == "__main__":
    __args__ = parse_cmd_arguments()
    # Set up the logger
    if int(__args__.debug) > 0:
        load_rentals_file = log_wrapper(load_rentals_file)
        calculate_additional_fields = log_wrapper(calculate_additional_fields)
        save_to_json = log_wrapper(save_to_json)
    logger.debug('Loading input file...')
    __data__ = load_rentals_file(__args__.input)
    logger.debug('Calculating data...')
    __data__ = calculate_additional_fields(__data__)
    logger.debug('Saving data...')
    save_to_json(__args__.output, __data__)
