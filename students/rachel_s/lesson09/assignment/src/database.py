#!/usr/bin/env python3

'''
Functions to add and remove items from furniture mongoDB, now with
decorators!
'''

# Rachel Schirra
# June 02, 2019
# Python 220 Lesson 09

import os
import csv
import argparse
from pymongo import MongoClient, InsertOne
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
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def log_wrapper(func):
    def logged(*args, **kwargs):
        if args and kwargs:
            logger.debug('Executing {function} with args {args}'
                         'and kwargs {kwargs}'.format(
                             function=func.__name__, args=args, kwargs=kwargs))
        elif args:
            logger.debug('Executing {function} with args {args}'.format(
                function=func.__name__, args=args))
        elif kwargs:
            logger.debug('Executing {function} with args {kwargs}'.format(
                function=func.__name__, kwargs=kwargs))
        else:
            logger.debug('Executing {function} with no arguments'.format(
                function=func.__name__
            ))
        result = func(*args, **kwargs)
        if result:
            logger.debug('Function {function} output: {result}'.format(
                function=func.__name__, result=result
            ))
        return result
    return logged


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


def bulk_writer(data, database, table):
    '''
    Accepts a dictionary of data, a database, and a table name. Bulk
    inserts the contents of the data set into the database in a table
    with the given name.
    Returns a tuple with the number of successful insertions and the
    number of insertion errors.
    '''
    logger.debug('Creating {} table'.format(table))
    my_db = database[table]
    logger.debug('Inserting data to {} table'.format(table))
    requests = []
    for item in data:
        requests.append(InsertOne(item))
    result = my_db.bulk_write(requests)
    try:
        result = my_db.bulk_write(requests)
    except BulkWriteError as err:
        logger.warning(err)
    logger.debug('{} records inserted to {} table'.format(
        result.bulk_api_result['nInserted'],
        table
    ))
    if result.bulk_api_result['writeErrors']:
        logger.warning('{} errors occurred on insertion to {} table'.format(
            len(result.bulk_api_result['writeErrors']),
            table
        ))
    else:
        logger.debug('{} errors occurred on insertion to {} table'.format(
            len(result.bulk_api_result['writeErrors']),
            table
        ))
    return (
        result.bulk_api_result['nInserted'],
        len(result.bulk_api_result['writeErrors'])
        )


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
        'customer': os.path.join(directory_name, customer_file),
        'product': os.path.join(directory_name, product_file),
        'rentals': os.path.join(directory_name, rentals_file)
    }

    mongo = MongoDBConnection()
    logger.debug('Connecting to MongoDB')
    with mongo:
        logger.debug('Connecting to hpnorton database')
        dbase = mongo.connection.hpnorton

        for name, path in paths.items():
            data = import_csv(path)
            try:
                result = bulk_writer(data, dbase, name)
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
    logger.debug('Connecting to MongoDB')
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
    logger.debug('Connecting to MongoDB')
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
    logger.debug('Connecting to MongoDB')
    with mongo:
        dbase = mongo.connection.hpnorton
        dbase.rentals.drop()
        logger.debug('Rentals dropped.')
        dbase.customer.drop()
        logger.debug('Customer dropped.')
        dbase.product.drop()
        logger.debug('Product dropped.')

def parse_cmd_arguments():
    """
    Takes command arguments and returns arguments as parsed according to
    the JSON file
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--debug', help='enable debugging',
                        default=0, required=False)
    return parser.parse_args()


if __name__ == "__main__":
    __args__ = parse_cmd_arguments()
    # Set up the logger
    if int(__args__.debug) > 0:
        show_rentals = log_wrapper(show_rentals)
        show_available_products = log_wrapper(show_available_products)
        import_data = log_wrapper(import_data)
        bulk_writer = log_wrapper(bulk_writer)
        import_csv = log_wrapper(import_csv)
