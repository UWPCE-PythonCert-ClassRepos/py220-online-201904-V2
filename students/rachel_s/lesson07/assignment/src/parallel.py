#!/usr/bin/env python3

'''Functions to add and remove items from furniture mongoDB'''

# Rachel Schirra
# May 22, 2019
# Python 220 Lesson 07

import os
import csv
import cProfile
import multiprocessing
import threading
import timeit
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

    mongo = MongoDBConnection()
    logger.debug('Connecting to MongoDB')
    with mongo:
        logger.debug('Connecting to hpnorton database')
        database = mongo.connection.hpnorton

        # LET'S DO SOME THREADS
        times_dict = {}

        prod_start_count = database.product.count_documents({})
        cust_start_count = database.customer.count_documents({})
        rent_start_count = database.rental.count_documents({})

        threads = [
            multiprocessing.Process(
                target=slow_writer,
                args=(
                    directory_name,
                    product_file,
                    database,
                    'product'
                )
            ),
            multiprocessing.Process(
                target=slow_writer,
                args=(
                    directory_name,
                    customer_file,
                    database,
                    'customer'
                )
            ),
            multiprocessing.Process(
                target=slow_writer,
                args=(
                    directory_name,
                    rentals_file,
                    database,
                    'rentals'
                )
            )
        ]

        for item in threads:
            item.start()

        for item in threads:
            item.join()

        prod_end_count = database.product.count_documents({})
        cust_end_count = database.customer.count_documents({})
        rent_end_count = database.rental.count_documents({})

        # Each module will return a list of tuples, one tuple for
        # customer and one for products. Each tuple will contain 4
        # values: the number of records processed (int), the record
        # count in the database prior to running (int), the record
        # count after running (int), and the time taken to run the
        # module (float).

    return([
        (
            prod_end_count - prod_start_count,
            prod_start_count,
            prod_end_count
        ),
        (
            cust_end_count - cust_start_count,
            cust_start_count,
            cust_end_count
        ),
        (
            rent_end_count - rent_start_count,
            rent_start_count,
            rent_end_count
        )
    ])


def show_available_products():
    '''
    Returns a python dictionary of products listed as available in the
    'product' collection. Contains the following fields:

    product_id
    description
    product_type
    quantity_available
    '''
    mongo = MongoDBConnection()
    logger.debug('Connecting to MongoDB')
    avail = []
    with mongo:
        logger.debug('Connecting to hpnorton database')
        database = mongo.connection.hpnorton
        records = database.product.find()
    for record in records:
        if int(record['quantity_available']) > 0:
            avail.append(
                {
                    'product_id': record['product_id'],
                    'description': record['description'],
                    'product_type': record['product_type'],
                    'quantity_available': record['quantity_available']
                }
            )
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
        database = mongo.connection.hpnorton
        renters = set()
        for item in database.rentals.find({'product_id': product_id}):
            renters.add(item['user_id'])
        records = {}
        for item in renters:
            renter = database.customer.find_one({'user_id': item})
            records[item] = renter
    return records


def db_clear():
    '''
    Deletes everything from all tables in the database.
    '''
    mongo = MongoDBConnection()
    logger.debug('Connecting to MongoDB')
    with mongo:
        database = mongo.connection.hpnorton
        database.rentals.drop()
        logger.debug('Rentals dropped.')
        database.customer.drop()
        logger.debug('Customer dropped.')
        database.product.drop()
        logger.debug('Product dropped.')


if __name__ == '__main__':
    db_clear()
    cProfile.run(
        'import_data("..\data", "product.csv", "customer.csv", "rental.csv")'
    )
