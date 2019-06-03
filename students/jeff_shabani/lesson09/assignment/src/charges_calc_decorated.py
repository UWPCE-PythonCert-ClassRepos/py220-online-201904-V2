'''
Returns total price paid for individual rentals
'''
import argparse
import json
import logging
from loguru import logger
import numpy as np
import pandas as pd

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)
LOGGER = logging.getLogger()


def parse_cmd_arguments():
    """
    parses command line arguments entered for debug level, source file name,
    and output file name.
    :return: arguments entered at command line
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s', '--log_switch', type=int, required=False,
                        metavar='', help='Turns logging on or off', default=1)
    parser.add_argument('-d', '--debug', type=int, required=False,
                        metavar='', help='Sets the logging level', default=0)
    parser.add_argument('-i', '--input', help='input JSON file',
                        required=False, default='source.json')
    parser.add_argument('-o', '--output', help='ouput JSON file',
                        required=False, default='output.json')

    args = parser.parse_args()
    return args


def logging_switch(option: int):
    """
    Decorator to turn logging on or off.
    :param option: int
    """
    logger.info(f'{logging_switch.__name__} arg is {option}')

    def dekorator(function):
        def wrapper(*args, **kwargs):
            if option:
                result = function(option)
            else:
                result = function(*args, **kwargs)
            return result

        return wrapper()

    return dekorator


@logging_switch
def configure_logging(log_level: int):
    """
    configures logging level based on args
    :param log_level:
    :return: logging objects with specified levels
    """
    logger.info(f'{configure_logging.__name__} arg in is {log_level}')
    if log_level == 0:
        LOGGER.disabled = True
    else:
        LOGGER.info(f'{configure_logging.__name__} Args are: {log_level}')
        log_file = logging.FileHandler('charges_calc.log')
        log_file.setFormatter(FORMATTER)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(FORMATTER)

        LOGGER.addHandler(log_file)
        LOGGER.addHandler(console_handler)

    if log_level == 1:
        LOGGER.setLevel(logging.ERROR)
    elif log_level == 2:
        LOGGER.setLevel(logging.WARNING)
    elif log_level == 3:
        LOGGER.setLevel(logging.DEBUG)
    else:
        return


def load_rentals_file(filename):
    """
    loads source json file
    :param filename:
    :return: dictionary of renter information
    """
    # pylint: disable=E1101, W1203
    logging.info(f'{filename} opened successfully')
    with open(filename) as file:
        logging.info(f'Filetype opened is {type(file)}')
        try:
            data = json.load(file)
        except FileNotFoundError:
            logging.error(f'{filename} does not exist.')
    return data


def calculate_additional_fields(data):
    """
    calculates new fields in renter information source file. Converts
    data dictionary to a pandas dataframe for easier field creation.
    :param data:
    :return: revised dataframe with new fields
    """
    # pylint: disable=W1203
    data_frame = pd.DataFrame.from_dict(data, orient='index')
    logging.info(f'{type(data_frame)} used to build new fields')
    data_frame['price_per_day'] = data_frame['price_per_day'].astype(float)
    data_frame['rental_start'] = pd.DatetimeIndex(data_frame['rental_start'])
    data_frame['rental_end'] = pd.DatetimeIndex(data_frame['rental_end'])

    # assure total days cannot be negative
    # pylint: disable=C0301
    data_frame['total_days'] = np.where(
        (data_frame['rental_start'] - data_frame['rental_end']) / np.timedelta64(1, 'D') < 0,
        (data_frame['rental_end'] - data_frame['rental_start']) / np.timedelta64(1, 'D'),
        (data_frame['rental_start'] - data_frame['rental_end']) / np.timedelta64(1, 'D') < 0)

    data_frame['total_price'] = data_frame['total_days'] * data_frame['price_per_day']
    data_frame['sqrt_total_price'] = np.sqrt(data_frame['total_price'])
    data_frame['unit_cost'] = data_frame['total_price'] / data_frame['units_rented']
    return data_frame


def save_to_json(filename, data):
    """
    converts dataframe to json format and writes to a new json file
    :param filename: based on args. Default is result.json
    :param data: dataframe created in calculate_additional_fields function
    :return: json file
    """
    # pylint: disable=E1101, W1203
    logging.info(f'File saved as {filename}')
    final = data.to_json(orient='index')
    try:
        with open(filename, 'w') as file:
            json.dump(final, file)
    except IOError:
        logging.error(f'{filename} was not written')


if __name__ == "__main__":
    INARGS = parse_cmd_arguments()
    logging_switch(INARGS.log_switch)
    DEBUG_LEVEL = INARGS.debug
    # configure_logging(DEBUG_LEVEL)
    SOURCE = load_rentals_file(INARGS.input)
    FINALDATA = calculate_additional_fields(SOURCE)
    save_to_json(INARGS.output, FINALDATA)
