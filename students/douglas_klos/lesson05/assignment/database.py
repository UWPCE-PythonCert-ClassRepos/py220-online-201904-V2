#!/usr/bin/env python3

import json
from pprint import pprint
import os
from loguru import logger
from bson import json_util
import src.mongodb_conn as mdb
from src.database_operations import drop_databases
import pymongo
import csv

mongo = mdb.MongoDBConnection()


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)


def import_data(directory_name, *files):

    _success = ()
    _fail = ()

    for csv_file in files:
        success, fail = insert_to_mongo(directory_name, csv_file)
        _success = _success + (success, )
        _fail = _fail + (fail, )

    return (_success, _fail)

    # Cheese mode to test the silly test
    # return ((10, 10, 9), (0, 0, 0))


def insert_to_mongo(directory_name, filename):

    success = 0
    fail = 0

    with mongo:
        db = mongo.connection.media
        logger.info(f"Inserting {filename[:-4]} into Mongo")
        database_name = db[filename[:-4]]

        iter_lines = get_line(open_file(f"{directory_name}{filename}"))
        header = next(iter_lines).split(',')

        if filename[:-4] != 'rental':
            database_name.create_index(header[0], unique=True)
        else:
            database_name.create_index([(header[0], pymongo.ASCENDING),
                                        (header[1], pymongo.ASCENDING)],
                                        unique=True)

        for line in iter_lines:
            line = line.split(',')
            new_addition = {}
            for num, field in enumerate(header):
                new_addition[field] = line[num]
            try:
                database_name.insert_one(new_addition)
                success += 1
            except pymongo.errors.DuplicateKeyError:
                fail += 1

    return success, fail


def show_available_products():
    logger.info(f"Preparing dict of available prodcuts...")
    available_products = {}

    with mongo:
        db = mongo.connection.media

        products = db['product']
        for doc in products.find():
            del(doc['_id'])
            if int(doc['quantity_available']) > 0:
                _doc = doc.copy()
                del(_doc['product_id'])
                available_products[doc['product_id']] =_doc

    return available_products


def show_rentals(product_id):
    logger.info(f"Perparing rental dict for product_id: {product_id}...")
    current_user_rentals = {}

    with mongo:
        db = mongo.connection.media

        # products = db['product']
        rentals = db['rental']
        customers = db['customers']

        # First we get a list of users that have the specified rental
        query = {"product_id": product_id}
        for rental in rentals.find(query):
            # Now we query customers user_id specified for the rental item.
            query = {"user_id": rental['user_id']}
            for customer in customers.find(query):
                _customer = customer.copy()
                del(_customer['_id'])
                del(_customer['user_id'])
                current_user_rentals[customer['user_id']] = _customer

    return current_user_rentals


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
        # next(content)  # Skip first line, it's the column names
        return content.read().decode("utf-8-sig", errors="ignore").split("\n")


def main(argv=None):
    """ database main function
    """
    pprint(drop_databases())
    pprint(import_data('./data/', 'product.csv', 'customers.csv', 'rental.csv'))
    pprint(show_available_products())
    pprint(show_rentals('prd002'))


if __name__ == "__main__":
    main()
