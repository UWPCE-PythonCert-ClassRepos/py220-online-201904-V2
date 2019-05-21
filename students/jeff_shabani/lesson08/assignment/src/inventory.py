"""
Module that creates new inventory management objects"""
from functools import partial
from pathlib import Path
import pandas as pd

DATA_PATH = Path.cwd().with_name('data')

COLUMNS = ['customer_name', 'item_code', 'item_description',
           'item_monthly_price']

SEED_DATA = [('Elisa Miles', 'LR04', 'Leather Sofa', 25.00),
             ('Susan Wong', 'FB31', 'Home Haircut Machine', 21.00),
             ('Edward Data', 'KT78', 'Kitchen Table', 10.00),
             ('Susan Wong', 'BT31', 'Flat-Screen TV', 200.00),
             ('Alex Gonzales', 'BR02', 'Queen Mattress', 17.00),
             ('Susan Wong', 'KT15', '5-Burner Stove', 175.00)]

TEST_FILE_NAME = 'test_items.csv'


def add_furniture(file_name, customer_name, item_code, item_description,
                  item_monthly_price):
    """
    This function creates a dataframe from an input source. It then checks if
    a file exists with an input name. If positive the found file is read in as a
    dataframe and the new data is appended and the file is resaved with the
    new data. If the csv does not previously exist it is created with the
    new data.
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
        test.to_csv(DATA_PATH / file_name, index=False)
    return test


def create_initial_file(file_name, source):
    """
    creates initial file for testing
    :param file_name:
    :param source:
    :return: csv file
    """
    test = pd.DataFrame.from_records(source, columns=COLUMNS)
    test.to_csv(DATA_PATH / file_name, index=False)


def check_file_exists(fpath_):
    """
    Function that checks if a file exists.
    :param fpath_
    :return: bool
    """
    return Path.exists(fpath_)


def single_customer(customer_name, dest_file_name, src_file_name):
    """
    This function takes a source csv and creates a new csv filtered to
    include only records with the customer name entered. It then uses funtools
    partial to create a new function with customer name and destination file
    name set. The only thing to enter is the name of the source file.
    :param customer_name:
    :param dest_file_name:
    :param src_file_name:
    :return: a new function
    """
    infile = pd.read_csv(DATA_PATH / src_file_name)
    infile = infile[infile['customer_name'] == customer_name]
    infile.to_csv(DATA_PATH / dest_file_name, index=False)


create_invoice = partial(single_customer, 'Susan Wong', 'rented_items.csv')

if __name__ == '__main__':
    create_initial_file(TEST_FILE_NAME, SEED_DATA)
    create_invoice('test_items.csv')
