#!/usr/bin/env python3

'''
Functions to add and remove items from furniture mongoDB
'''

# Rachel Schirra
# June 02, 2019
# Python 220 Lesson 09

import os
import csv
import cProfile
from pymongo import MongoClient
from pymongo.errors import PyMongoError, BulkWriteError
from loguru import logger


class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        # Let's move the logging for mongodb connections out of the code
        # and put it here instead so we don't have it laying around all
        # over the place.
        logger.debug('Connecting to MongoDB.')
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Report the values when we exit also
        logger.debug(f'exc_type: {exc_type}')
        logger.debug(f'exc_val: {exc_val}')
        logger.debug(f'exc_traceback: {exc_tb}')
        self.connection.close()


def import_csv(path):
    '''
    Accepts a path to a CSV file.
    Returns a list of dictionaries with the contents of that CSV file.
    Uses file headers as field names.
    '''
    file_dicts = []
    logger.debug('Attempting to open file {}'.format(path))
    with open(path, encoding='utf-8-sig') as file:
        try:
            csv_reader = csv.DictReader(file, delimiter=',')
            logger.debug('Successfully loaded {}'.format(path))
            for row in csv_reader:
                file_dicts.append(dict(row))
        except(FileNotFoundError, ValueError) as err:
            logger.error(err)
    return file_dicts


def slow_writer(directory_name, data_file, database, table):
    '''
    When I profiled this using the bulk_writer function it turned up a
    whole load of threading.py processes. Also I have noticed that it is
    quite speedy. I infer that pymongo.bulk_write is in fact already
    using threading for speed.
    So now I have to rewrite my database insertion to be less efficient
    and insert records one at a time so I can go back and add the
    concurrency myself.
    Ah, such is life.

    Accepts a dictionary of data, a database, and a table name. Bulk
    inserts the contents of the data set into the database in a table
    with the given name.
    Returns a tuple with the number of successful insertions and the
    number of insertion errors.
    '''

    logger.debug('Converting {} file to dictionary'.format(table))
    data = import_csv(os.path.join(
        directory_name,
        data_file
        ))

    logger.debug('Creating {} table'.format(table))
    my_db = database[table]
    logger.debug('Inserting data to {} table'.format(table))
    errors = 0
    writes = 0
    for item in data:
        try:
            my_db.insert_one(item)
            writes += 1
        except PyMongoError as err:
            logger.warning(err)
            errors += 1
    logger.debug('{} records inserted to {} table'.format(
        writes,
        table
    ))
    return (writes, errors)


def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Takes a directory name and three CSV files and creates and populates
    a new MongoDB database containing that data.

    Returns 2 tuples: A record count of the number of products,
    customers, and rentals added, and a count of any errors that
    occurred.
    '''
    records = {'customer': 0,
               'product': 0,
               'rentals': 0}
    error_count = {'customer': 0,
                   'product': 0,
                   'rentals': 0}
    paths = {
        'customer': customer_file,
        'product': product_file,
        'rentals': rentals_file
    }

    mongo = MongoDBConnection()
    with mongo:
        logger.debug('Connecting to hpnorton database')
        dbase = mongo.connection.hpnorton

        for name, filename in paths.items():
            try:
                # (directory_name, data_file, database, table):
                result = slow_writer(directory_name, filename, dbase, name)
                records[name] = result[0]
                error_count[name] = result[1]
            except BulkWriteError as err:
                logger.error(err)

    return ((records['product'], records['customer'], records['rentals']),
            (error_count['product'], error_count['customer'],
             error_count['rentals']))


def show_available_products():
    '''
    Returns a python dictionary of products listed as available in the
    'product' collection.

    Args:
        product_id (str): Alphanumeric product ID
        description (str): Description of the item
        product_type (str): The product type
        quantity_available (int): How many are available
    '''
    mongo = MongoDBConnection()
    avail = {}
    with mongo:
        logger.debug('Connecting to hpnorton database')
        dbase = mongo.connection.hpnorton
        records = dbase.product.find()
    for record in records:
        if int(record['quantity_available']) > 0:
            name = record['product_id']
            del record['_id']
            del record['product_id']
            avail[name] = record
    return avail


def show_rentals(product_id):
    '''
    Takes a product ID.
    Returns a dictionary containing all customers who have rented that
    item, with the following fields:

    user_id
    name
    address
    phone number
    email
    '''
    mongo = MongoDBConnection()
    with mongo:
        logger.debug('Connecting to hpnorton database')
        dbase = mongo.connection.hpnorton
        renters = set()
        for item in dbase.rentals.find({'product_id': product_id}):
            renters.add(item['user_id'])
        records = {}
        for item in renters:
            renter = dbase.customer.find_one({'user_id': item})
            name = renter['user_id']
            del renter['_id']
            del renter['user_id']
            del renter['zip_code']
            records[name] = renter
    return records


def db_clear():
    '''
    Deletes everything from all tables in the database.
    '''
    mongo = MongoDBConnection()
    with mongo:
        dbase = mongo.connection.hpnorton
        dbase.rentals.drop()
        logger.debug('Rentals dropped.')
        dbase.customer.drop()
        logger.debug('Customer dropped.')
        dbase.product.drop()
        logger.debug('Product dropped.')


if __name__ == "__main__":
    cProfile.run(
        'import_data("../tests", "products.csv", "customers.csv", "rentals.csv")'
    )
