'''
Uses previously gathered inventory and rental data to calculate new fields.

I have a logging message in place to inform a user if their json file has
errors preventing it from being loaded at all.
As well a a message to inform users of errors within a loaded json file that
will result in bad output.
If the debug level is set to 3 (logging.DEBUG in this case) debug messages will
be shown in the console describing where in the process the program
is.
'''

import argparse
import json
import datetime
import math
import logging


def parse_cmd_arguments():# {{{
    """ Parse arguments entered at command line. """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output',
                        help='ouput JSON file', required=True)
    parser.add_argument('-d', '--loglevel', nargs='?',
                        const='0', help='logging level')

    return parser.parse_args()# }}}


def logging_level_decorator(func):# {{{
    """ Logging level wrapper to decorate other functions with. """
    def turn_on_logging(*args, **kwargs):
        """
        This will set the debug level based on the debug argument
        passed in by the user at the command line.
        """
        if int(ARGS.loglevel) > 3:
            ARGS.loglevel = '3'
        log_levels = {'1': logging.ERROR, '2': logging.WARNING,
                      '3': logging.DEBUG}
        log_format = ("\n%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s"
                      "\n%(message)s")

        formatter = logging.Formatter(log_format)

        log_file = 'data/' + datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_levels[ARGS.loglevel])
        console_handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.setLevel(log_levels[ARGS.loglevel])
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logging.debug(("Debug set to: %s\n"
                       "Log messages will be stored in:\n"
                       "%s\n"
                       "In the current directory."), ARGS.loglevel, log_file)

        data_to_return = func(*args, **kwargs)
        logger.setLevel(log_levels['1'])

        return data_to_return
    return turn_on_logging# }}}


@logging_level_decorator
def load_rentals_file(filename):# {{{
    """
    This will load the json file based on the filename provided
    by the user at the command line.
    """
    with open(filename) as file:
        logging.debug("At start of load_rentals_file.")
        try:
            in_file = json.load(file)

        except json.JSONDecodeError as json_error:
            logging.error(("Critical error unable to load file: %s\n"
                           "This error needs to be fixed before"
                           " any data can be processed.\n"
                           "Json error message: %s\n"
                           "Line Number: %s\n"
                           "Column Number: %s"), filename, json_error.msg,
                          json_error.lineno, json_error.colno)
            exit(1)

    logging.debug("Json file loaded successfully, returning loaded file.")
    return in_file# }}}


@logging_level_decorator
def calculate_additional_fields(data):# {{{
    """
    Calculates and adds additional fields to the existing json
    structure.
    """
    logging.debug("At start of calculate_additional_fields")
    error_dict = {}

    for key, value in data.items():
        try:
            rental_start = datetime.datetime.strptime(
                value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(
                value['rental_end'], '%m/%d/%y')
            # Ok, so sometimes the rental_start and end are mixed up.
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            # I'm not sure why we need the sqrt of total price... But it is
            # throwing an error since our total_price was negative.
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except ValueError:
            error_dict[key] = value
            logging.warning(("Error in input file: %s\n"
                             "Program will continue and process all "
                             "unaffected data. Affected data will not "
                             "be included.\n"
                             "Item Number: %s\n"
                             "Item Info:\n%s"), ARGS.input, key, value)

    for key in error_dict:
        del data[key]

    logging.debug("json file processed returning with additional fields.")
    return data# }}}


@logging_level_decorator
def save_to_json(filename, data):# {{{
    """
    Saves data to a new file based on the output variable provided
    by the user at the command line.
    """
    logging.debug("At start of save_to_json.")
    with open(filename, 'w') as file:
        json.dump(data, file)# }}}


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.input)
    DATA = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA)
