'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOGGER = logging.getLogger()

def parse_cmd_arguments():
    '''
    Parses arguments from the commandline when run
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

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


def load_rentals_file(filename):
    '''
    Loads rental data from a file on the system.
    '''
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            exit(0)

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
