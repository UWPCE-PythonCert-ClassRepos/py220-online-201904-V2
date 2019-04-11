'''
Returns total price paid for individual rentals 
'''
import argparse
import json
import datetime
import math
import logging


def parse_cmd_arguments():
    # I'm a little confused about how argparse works but have determined that
    # add_argument below creates two positional arguments required at the time
    # the script is called in the command line.
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug',nargs='?', const='0', help='debug level')

    return parser.parse_args()


def turn_on_debug(debug_level):
    debug_levels = {'1': logging.ERROR, '2': logging.WARNING, '3': logging.DEBUG}
    log_format  = "%(levelname)s %(asctime)s %(filename)s:%(lineno)-4d \n%(message)s"

    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(debug_levels[debug_level])
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(debug_levels[debug_level])
    logger.addHandler(console_handler)


def load_rentals_file(filename):
    with open(filename) as file:
        # Ok, so there's a typo in the source.json file. Need to set up a
        # logging message that will inform the user of the error if they have
        # debug messages turned on and without crashing the program.
        try:
            data = json.load(file)

        # It took me a while but I figured out how to access the error's
        # attributes.
        except json.JSONDecodeError as json_error: 
            logging.error(("Error processing json file.\n"
                "Json error message: {}\n"
                "Line Number: {}\n"
                "Column Number: {}").format(json_error.msg, json_error.lineno, json_error.colno))
            exit(1)

    return data

def calculate_additional_fields(data):
    print("in first line of calculate_additional_fields")
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
    if args.debug:
        turn_on_debug(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
