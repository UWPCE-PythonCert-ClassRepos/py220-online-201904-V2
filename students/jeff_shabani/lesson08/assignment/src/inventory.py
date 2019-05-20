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

SEED_DATA_3 = [('3Elisa Miles', 'LR04', 'Leather Sofa', 25.00),
               ('3Edward Data', 'KT78', 'Kitchen Table', 10.00),
               ('3Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)]


def add_furniture(file_name, source):
    """
    This function creates a dataframe from an input source. It then checks if
    a with an input file name exists. If it is read in as a dataframe and the
    new data is appended and the file is resaved with the new data. If the csv
    does not previously exist it is created with the new data.
    :param file_name:
    :param source:
    :return: new or modified csv file
    """
    test = pd.DataFrame.from_records(source, columns=COLUMNS)
    test['invoice_file'] = file_name
    if check_file_exists(DATA_PATH / file_name):
        read_in = pd.read_csv(DATA_PATH / file_name)
        read_in = read_in.append(test)
        read_in.to_csv(DATA_PATH / file_name, index=False)
    else:
        final = test.to_csv(DATA_PATH / file_name, index=False)
    return test


def check_file_exists(fpath_):
    """
    Function that checks if a file exists.\
    :param fpath_:
    :return: bool
    """
    return Path.exists(fpath_)

def single_customer():
    pass


if __name__ == '__main__':
    add_furniture('inventory.csv', SEED_DATA)
