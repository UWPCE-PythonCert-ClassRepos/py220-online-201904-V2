#!/usr/bin/env python3

from loguru import logger
from mongoengine import *
from pymongo.errors import DuplicateKeyError
from src.models import Customers
from src.models import Product
from src.models import Rental

connect('mongoengine')

# customer = Customers.objects.first()
# print(customer)
# print(customer.to_json())
# print(Customers.objects(user_id='user001)'))


def insert_to_mongo(directory_name, filename):
    """Inserts given csv file into mongo

    Arguments:
        directory_name {string} -- directory containing csv file
        filename {string} -- csv filename to import

    Returns:
        int, int -- success / fails of imports
    """

    # This is a pretty cool function. Based on the file that sent in, it needs
    #   to access different classes.  The class name can be derived from the
    #   filename[:-4].title().

    success = 0
    fail = 0

    logger.info(f"Inserting {filename[:-4]} into Mongo...")
    _class = filename[:-4].title()

    iter_lines = get_line(open_file(f"{directory_name}{filename}"))
    header = next(iter_lines).split(",")

    for line in iter_lines:
        line = line.split(",")
        new_addition = {}
        for num, field in enumerate(header):
            new_addition[field] = line[num]
        try:
            # We need to call the class _class on new_addition dynamically.
            obj = globals()[_class](**new_addition)
            obj.save()
            success += 1
        except NotUniqueError as ex:
            fail += 1

    return success, fail


def import_data(directory_name, *files):
    """Import csv files into mongodatabase.

    Arguments:
        directory_name {string} -- directory data files are stored in
        *files {list} -- *args list of csv files to import

    Returns:
        ((),()) -- Tuple of Tuples, ((Success),(Failures)) from imports
    """
    _success = ()
    _fail = ()

    for csv_file in files:
        success, fail = insert_to_mongo(directory_name, csv_file)
        _success = _success + (success,)
        _fail = _fail + (fail,)

    return (_success, _fail)

    # Cheese mode to test the silly test
    # return ((10, 10, 9), (0, 0, 0))


def get_line(lines):
    """Generator for lines of content from csv file

    Arguments:
        lines {list} -- List of lines containing data from csv file

    Yields:
        string -- CSV string containing information for a single customer.
    """
    for line in lines:
        yield line


def open_file(filename):
    """Opens the file specified from the command line

    Arguments:
        filename {string} -- Name of CSV file to import

    Returns:
        list containing lines of customer data from csv file
    """
    # I'm assuming pythons garbage collection takes care of closing the file.
    with open(filename, "rb") as content:
        return content.read().decode("utf-8-sig", errors="ignore").split("\n")
