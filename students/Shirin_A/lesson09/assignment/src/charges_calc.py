""" Returns total price paid for individual rentals"""
# pylint: disable=C0303
import argparse
import json
import datetime
import math
import logging

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOGGER = logging.getLogger()


def disable_logging(func):
    """Decorator to turns off logging in functions
    """
    def wrapper(*args, **kwargs):

        LOGGER.disabled = True

        result = func(*args, **kwargs)

        LOGGER.disabled = False        
        return result
    return wrapper


def setup_log_level(log_level):
    """
    Configures the logging
    Sets different log levels for debugger
    :paramater log_levels: 1(Error), 2(Debug), 3(Warning)
    :return:

    """
    # Breakdown of what will be returned under each level
    if log_level == 0:
        return
    log_file = 'charges_calc.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(FORMATTER)
    LOGGER.addHandler(file_handler)
    if log_level == 1:
        print('debug on, error only')
        LOGGER.setLevel(logging.ERROR)
        file_handler.setLevel(logging.ERROR)
    elif log_level == 2:
        print('error messages and warnings')
        LOGGER.setLevel(logging.WARNING)
        file_handler.setLevel(logging.WARNING)
    elif log_level == 3:
        print('error messages, warnings and debug messages')
        LOGGER.setLevel(logging.DEBUG)      
   

def parse_cmd_arguments():
    """Parses commands from the commandline"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument(
        '-d', '--debug', help='debug_logging_level_help', required=False)

    return parser.parse_args()

@disable_logging
def load_rentals_file(filename):
    """
    function to load input file, exits if issues are found with the input file
    """
    logging.debug("Opening file %s", filename)
    with open(filename) as file:
        try:
            data = json.load(file)
            logging.debug("JSON has successfully loaded")            
        except ValueError as err:
            logging.error("Error reading input file %s", file)
            print(f"Error reading the input file: {err}")                    
            exit(0)       
    return data

@disable_logging
def calculate_additional_fields(data):
    '''
    Calculate additional fields based on source.json file
    '''
    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
        except ValueError:
            logging.warning("rental start has an invalid rental date value %s", key)
            logging.debug("Occurred in calculate_additional_fields method")
        try:
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError:
            logging.warning("rental end has an invalid rental date value %s", key)
            logging.debug("Occurred in calculate_additional_fields method")
        value['total_days'] = (rental_end - rental_start).days
        if value['total_days'] < 0:
            logging.warning("rental start is before the rental end in %s", key)
            logging.debug("Occurred in calculate_additional_fields method")
        try:
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError as ex:
            if "math domain error" in str(ex):
                logging.error('''total_price is negative: %s for %s, sqrt_total_price \

and unit_cost may be omitted''', value["total_price"], key)
                logging.debug("Occurred in calculate_additional_fields method")
            elif 'does not match format' in str(ex):
                logging.warning(ex)
                logging.debug("Occurred in calculate_additional_fields method")
    return data

@disable_logging
def save_to_json(filename, data):
    """function to save calculated values from calculate_additional_fields()
       into an output JSON file,name specified in parse_cmd_arguments()"""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except FileNotFoundError:
        logging.error("Can't locate requested file")
        #logging.debug("Occurred in load_rentals_file method")
        
if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DEBUG_LEVEL = int(ARGS.debug)
    setup_log_level(DEBUG_LEVEL)
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
