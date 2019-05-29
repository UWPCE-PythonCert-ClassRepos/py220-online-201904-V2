'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
from pathlib import Path
import math
import logging
from undecorated import undecorated

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)
LOGGER = logging.getLogger()



def parse_cmd_arguments():
    '''
    Parses arguments from the commandline when run
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file',
                        required=True)
    parser.add_argument('-d', '--debug', help='enable debug logging',
                        required=False, default=0)
    return parser.parse_args()


def log_level_settings(log_level):
    '''
    This will set the log levels we're going to use.  We'll be using ERROR,
    WARNING, and DEBUG, and OFF
    0 = Off       Adding these because first idea of strings was bad I guess.
    1 = ERROR
    2 = WARNING
    3 = DEBUG
    '''
    # if log_level == 'OFF': Well that doesn't work.
    log_file = logging.FileHandler('charges_calc.log')
    log_file.setFormatter(FORMATTER)
    LOGGER.addHandler(log_file)

    if log_level == 1:
        LOGGER.setLevel(logging.ERROR)
    elif log_level == 2:
        LOGGER.setLevel(logging.WARNING)
    elif log_level == 3:
        LOGGER.setLevel(logging.DEBUG)
    else:
        return


def conditional_log(func):
    '''
    Decorator for conditional logging.
    '''
    def not_logged(*args, **kwargs):
        logging.disable(logging.CRITICAL)  # Turn logging off
        result = func(*args, **kwargs)  # Run function
        logging.disable(logging.NOTSET)  # Turn logging on
        return result
    return not_logged


def load_rentals_file(filename):
    '''
    Loads rental data from a file on the system.
    '''
    filename = Path.cwd().with_name('data') / filename
    with open(filename) as file:
        try:
            data = json.load(file)
            # import pdb; pdb.set_trace()
        except ValueError as err_code:
            logging.error('Error reading file %s', file)
            print(f'Error reading the file: {err_code}')
            exit(0)
    # import pdb; pdb.set_trace()
    return data


@conditional_log
def calculate_additional_fields(data):
    '''
    Calculate fields from the file.  To be honest at this stage I don't know
    what it actually does.
    '''
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
        except ValueError as date_error:
            logging.error('%s Incorrect date formatting.', date_error)
            print(f'Date format is incorrect. m/d/y is correct.')
            logging.debug(value)

        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.error('Total days is negative.')
            print('Total days cannot be negative.')
            logging.debug(value)

        value['total_price'] = value['total_days'] * value['price_per_day']

        try:
            value['sqrt_total_price'] = math.sqrt(value['total_price'])

        except ValueError as math_domain_error:
            logging.error('%s Unable to calculate.', math_domain_error)
            print('Square root of negative number attempted.')
            logging.debug(value)

        try:
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ZeroDivisionError as div_error:
            logging.warning('%s division by 0.', div_error)
            print('Error with units rented. Division by 0.')
            logging.debug(value)

        # import pdb; pdb.set_trace()
#        except:
#            exit(0)
#            import pdb; pdb.set_trace()
    return data


def save_to_json(filename, data):
    '''
    Does what it says on the tin.  Saves a json file.
    '''
    logging.debug('Saving file %s', filename)
    with open(filename, 'w') as file:
        # import pdb; pdb.set_trace()
        json.dump(data, file)


if __name__ == '__main__':
    ARGS = parse_cmd_arguments()
    DEBUG_LEVEL = int(ARGS.debug)
    log_level_settings(DEBUG_LEVEL)
    DATA = load_rentals_file(ARGS.input)
    if int(ARGS.conditional) == 1:
        FINAL_DATA = calculate_additional_fields(DATA)
    else:
        PLAIN_FUNC = undecorated(calculate_additional_fields)
        FINAL_DATA = PLAIN_FUNC(DATA)

    save_to_json(ARGS.output, FINAL_DATA)
