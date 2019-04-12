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

def setup_log_level(log_level):
    """
    Sets log level for debugger
    :param log_level: 0, 1, 2, or 3
    :return:
    """
    if log_level == 0:
        return
    file_handler = logging.FileHandler('charges_calc.log')
    file_handler.setFormatter(FORMATTER)
    LOGGER.addHandler(file_handler)
    
    if log_level == 1:
        LOGGER.setLevel(logging.ERROR)
    elif log_level == 2:
        LOGGER.setLevel(logging.WARNING)
    elif log_level == 3:
        LOGGER.setLevel(logging.DEBUG)
        
def load_rentals_file(filename):
    """
    Load rental data from source file.
    :param filename: source file
    :return: data
    """
    logging.debug("Opening file %s", filename)
    with open(filename) as file:
        try:
            data = json.load(file)
        except ValueError as err:
            logging.error("Error reading input file %s", file)
            print(f"Error reading the input file: {err}")
            exit(0)
    return data

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
