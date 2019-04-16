'''
<<<<<<< HEAD
Returns total price paid for individual rentals
'''
#!/usr/bin/env python3

=======
Returns total price paid for individual rentals 
'''
>>>>>>> ff1f77f678e19a269542ef82af223e77e047410e
import argparse
import json
import datetime
import math
<<<<<<< HEAD
import logging

LOG_FILE = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

#warning and above to log file
FILE_HANDLER = logging.FileHandler('charges_calc.log')
#FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

#all loggin message at console
CONSOLE_HANDLER = logging.StreamHandler()
#CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
#LOGGER.setLevel(logging.DEBUG)
#LOGGER.addHandler(FILE_HANDLER)
#LOGGER.addHandler(CONSOLE_HANDLER)

def parse_cmd_arguments():
    '''parse command line arguments'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug levels', required=True)
    return parser.parse_args()

def logging_levels(debug_level):
    '''setting logging level for file_handler'''

    if debug_level == '1':
        #1: Only error messages.
        LOGGER.setLevel(logging.ERROR)
        FILE_HANDLER.setLevel(logging.ERROR)
        CONSOLE_HANDLER.setLevel(logging.ERROR)
    elif debug_level == '2':
        #2: Error messages and warnings.
        LOGGER.setLevel(logging.WARNING)
        FILE_HANDLER.setLevel(logging.WARNING)
        CONSOLE_HANDLER.setLevel(logging.WARNING)
    elif debug_level == '3':
        #3: Error messages, warnings and debug messages.
        LOGGER.setLevel(logging.DEBUG)
        FILE_HANDLER.setLevel(logging.DEBUG)
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
    elif debug_level == '0':
        return
    LOGGER.addHandler(FILE_HANDLER)
    LOGGER.addHandler(CONSOLE_HANDLER)


def load_rentals_file(filename):
    '''load input file to data'''
    with open(filename) as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            logging.error('json file load error')
=======

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
>>>>>>> ff1f77f678e19a269542ef82af223e77e047410e
            exit(0)
    return data

def calculate_additional_fields(data):
<<<<<<< HEAD
    '''sss'''
    for key, value in data.items():
        try:
            if value['rental_start'] == '' or value['rental_end'] == '':
                logging.warning('For %s, rental end/start day is missing, '
                                'skip entry.', key)
                continue
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
            if rental_end < rental_start:
                logging.debug('For %s, rental end day is prior to rental '
                              'start date, swap date.', key)
                rental_start = datetime.datetime.strptime(value['rental_end'],
                                                          '%m/%d/%y')
                rental_end = datetime.datetime.strptime(value['rental_start'],
                                                        '%m/%d/%y')
=======
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
>>>>>>> ff1f77f678e19a269542ef82af223e77e047410e
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
<<<<<<< HEAD
        except ZeroDivisionError:
            logging.warning('For %s, units rented is 0, skip entry.', key)
            continue

=======
        except:
            exit(0)
>>>>>>> ff1f77f678e19a269542ef82af223e77e047410e

    return data

def save_to_json(filename, data):
<<<<<<< HEAD
    '''write data to output file'''
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    logging_levels(ARGS.debug)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
=======
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
>>>>>>> ff1f77f678e19a269542ef82af223e77e047410e
