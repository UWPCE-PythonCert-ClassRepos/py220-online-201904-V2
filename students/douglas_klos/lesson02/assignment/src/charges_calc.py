#!/usr/bin/env python3
"""Returns total price paid for individual rentals"""
import argparse
import json
import datetime
import math
import logging


log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def parse_cmd_arguments():
    logging.info('Start of parse_cmd_arguments()')
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debugger level', required=False)

    return parser.parse_args()


def load_rentals_file(filename):
    logging.info('-----Start of load_rental_file-----')
    with open(filename) as file:
        try:
            data = json.load(file)
        except Exception as e:
            logging.critical(f'Loading data from json failed.\n\tException: {repr(e)}')
            exit(0)
    return data

def repair_dates(data):
    logging.info('-----Start of repair_dates-----')
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            if rental_end < rental_start:
                logging.warning(f'Key:{key} rental start, end dates reversed.  Repairing.')
                value['rental_start'], value['rental_end'] = value['rental_end'], value['rental_start']
        except ValueError:
            logging.error(f'Key:{key} contains bad date data.  Skipping.')
            logging.debug(f'Value:{value}')

    return data


def calculate_additional_fields(data, bad_data):
    logging.info('-----Start of load_additional_fields-----')
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except Exception as e:
            bad_data[key] = value
            logging.error(f'Key:{key} Failed calculating additional fields.  Skipping.')
            logging.debug(f'Value:{value}')

    return data, bad_data


def remove_bad_data(data, bad_data):
    for key in bad_data:
        del data[key]
    
    return data, bad_data


def save_to_json(filename, data):
    logging.info('-----Start of save_to_json(filename, data)-----')
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    bad_data = {}
    args = parse_cmd_arguments()
    data = load_rentals_file(args.input)
    data = repair_dates(data)
    data, bad_data = calculate_additional_fields(data, bad_data)
    data, bad_data = remove_bad_data(data, bad_data)
    save_to_json(args.output, data)
    save_to_json('bad_data.json', bad_data)
