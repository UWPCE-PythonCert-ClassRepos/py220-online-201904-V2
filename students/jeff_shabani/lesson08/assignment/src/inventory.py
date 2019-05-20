"""
Module that creates new inventory management objects"""
from functools import partial
from pathlib import Path
import pandas as pd

DATA_PATH = Path.cwd().with_name('data')

COLUMNS = ['customer_name', 'item_code', 'item_description',
           'item_monthly_price']

SEED_DATA = [('Elisa Miles', 'LR04', 'Leather Sofa', 25.00),
             ('Edward Data', 'KT78', 'Kitchen Table', 10.00),
             ('Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)]

TEST_FILE_NAME = 'test_items.csv'


def add_furniture(file_name, customer_name, item_code, item_description,
           item_monthly_price):
    """
    This function creates a dataframe from an input source. It then checks if
    a with an input file name exists. If it is read in as a dataframe and the
    new data is appended and the file is resaved with the new data. If the csv
    does not previously exist it is created with the new data.
    :param file_name:
    :param source:
    :return: new or modified csv file
    """

    data = [(customer_name, item_code, item_description,
           item_monthly_price)]
    test = pd.DataFrame.from_records(data, columns=COLUMNS)
    if check_file_exists(DATA_PATH / file_name):
        read_in = pd.read_csv(DATA_PATH / file_name)
        read_in = read_in.append(test)
        read_in.to_csv(DATA_PATH / file_name, index=False)
    else:
        final = test.to_csv(DATA_PATH / file_name, index=False)
    return test


def create_initial_file(file_name, source):
    """
    creates initial file for testing
    :param file_name:
    :param source:
    :return: csv file
    """
    test = pd.DataFrame.from_records(source, columns=COLUMNS)
    return test.to_csv(DATA_PATH / file_name, index=False)


def check_file_exists(fpath_):
    """
    Function that checks if a file exists.
    :param fpath_:
    :return: bool
    """
    return Path.exists(fpath_)

def single_customer(customer_name, file_name):
    pass


if __name__ == '__main__':
    create_initial_file(TEST_FILE_NAME, SEED_DATA)
    add_furniture(TEST_FILE_NAME, 'New Person 1', 'LR04', 'Leather Sofa', 25.00)
    add_furniture(TEST_FILE_NAME, 'New Person 2', 'LR04', 'Leather Sofa', 25.00)
