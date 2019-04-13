'''
Returns total price paid for individual rentals
'''

import argparse
import json
import datetime
import math

def parse_cmd_arguments():
    """
    Takes command arguments and returns arguments as parsed according to
    the JSON file
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)

    return parser.parse_args()


def load_rentals_file(filename):
    """
    Loads rentals JSON file and exits with a FileNotFoundError if it
    encounters a problem.
    """
    with open(filename) as file:
        try:
            rentals = json.load(file)
        except FileNotFoundError:
            exit(0)
    return rentals

def calculate_additional_fields(rental_data):
    """
    Accepts a rental_data JSON file.
    Calculates total days of rental, total price, and unit cost. Exits
    if a key is not found in rental_data.
    """
    for value in rental_data.values():
        try:
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
        except KeyError:
            exit(0)

    return rental_data

def save_to_json(filename, rental_data):
    """
    Saves modified rental data as JSON with the specified file name.
    """
    with open(filename, 'w') as file:
        json.dump(rental_data, file)

if __name__ == "__main__":
    __args__ = parse_cmd_arguments()
    __data__ = load_rentals_file(__args__.input)
    __data__ = calculate_additional_fields(__data__)
    save_to_json(__args__.output, __data__)
