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
    log_format  = ("\n%(levelname)s %(asctime)s"
    "%(filename)s:%(lineno)-4d\n%(message)s")

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
        logging.debug("At start of load_rentals_file.")
        try:
            data = json.load(file)

        # It took me a while but I figured out how to access the error's
        # attributes.
        except json.JSONDecodeError as json_error: 
            logging.error(("Critical error unable to load file: {}\n"
                "This error needs to be fixed before any data can be processed.\n"
                "Json error message: {}\n"
                "Line Number: {}\n"
                "Column Number: {}").format(filename, json_error.msg, json_error.lineno, json_error.colno))
            exit(1)

    return data

def calculate_additional_fields(data):
    logging.debug("At start of calculate_additional_fields")
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            # Ok, so sometimes the rental_start and end are mixed up.
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            # I'm not sure why we need the sqrt of total price... But it is
            # throwing an error since our total_price was negative.
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as value_error:
            logging.warning(("\nError in input file: {}\n"
            "Program will continue and process all unaffected data.\n"
            "Item with error will be included in output but will "
            "have errors or missing data. Fix the error in the "
            "source file and rerun to fix errors in output.\n"
            "Item number: {}\n"
            "Item info:\n{}").format(args.input, key, value))

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
