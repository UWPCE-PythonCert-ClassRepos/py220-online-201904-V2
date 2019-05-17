#!/usr/bin/env python3

'''Functions to add and remove items from furniture mongoDB'''

# Rachel Schirra
# May 4, 2019
# Python 220 Lesson 05

import os
import csv
from pymongo import MongoClient, InsertOne
from pymongo.errors import BulkWriteError
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

'''
import_data(directory_name, product_file, customer_file, rentals_file):

This function takes a directory name three csv files as input, one with
product data, one with customer data and the third one with rentals data
and creates and populates a new MongoDB database with these data. It
returns 2 tuples: the first with a record count of the number of
products, customers and rentals added (in that order), the second with a
count of any errors that occurred, in the same order.
'''

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
    if len(result.bulk_api_result['writeErrors']) > 0:
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

    logger.debug('Converting products file to dictionary')
    product_dict = import_csv(os.path.join(
        directory_name,
        product_file
        ))

    logger.debug('Converting customers file to dictionary')
    customer_dict = import_csv(os.path.join(
        directory_name,
        customer_file
        ))

    logger.debug('Converting rentals file to dictionary')
    rentals_dict = import_csv(os.path.join(
        directory_name,
        rentals_file
        ))

    mongo = MongoDBConnection()
    logger.debug('Connecting to MongoDB')
    with mongo:
        logger.debug('Connecting to hpnorton database')
        db = mongo.connection.hpnorton

        # Create product data collection
        try:
            prod_result = bulk_writer(product_dict, db, 'product')
            records['product'] = prod_result[0]
            error_count['product'] = prod_result[1]
        except BulkWriteError as err:
            logger.error(err)
            records['product'] = err.details['nInserted']
            error_count['product'] = len(err.details['writeErrors'])

        # Create customer data collection
        try:
            cust_result = bulk_writer(customer_dict, db, 'customer')
            records['customer'] = cust_result[0]
            error_count['customer'] = cust_result[1]
        except BulkWriteError as err:
            logger.error(err)
            records['customer'] = err.details['nInserted']
            error_count['customer'] = len(err.details['writeErrors'])

        # Create rentals data collection
        try:
            rent_result = bulk_writer(rentals_dict, db, 'rentals')
            records['rentals'] = rent_result[0]
            error_count['rentals'] = rent_result[1]
        except BulkWriteError as err:
            logger.error(err)
            records['rentals'] = err.details['nInserted']
            error_count['rentals'] = len(err.details['writeErrors'])

    return ((records['product'], records['customer'], records['rentals']),
            (error_count['product'], error_count['customer'],
             error_count['rentals']))


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
        db = mongo.connection.hpnorton
        records = db.product.find()
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


'''
show_available_products(): 
Returns a Python dictionary of products listed as available with the
following fields:

product_id.
description.
product_type.
quantity_available.

For example:

{‘prd001’:
    {‘description’:‘60-inch TV stand’,
    ’product_type’:’livingroom’,
    ’quantity_available’:‘3’},
    ’prd002’:{‘description’:’L-shaped sofa’,
    ’product_type’:’livingroom’,
    ’quantity_available’:‘1’}
    }
'''

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
        db = mongo.connection.hpnorton
        renters = set()
        for item in db.rentals.find({'product_id': product_id}):
            renters.add(item['user_id'])
        records = {}
        for item in renters:
            renter = db.customer.find_one({'user_id': item})
            del renter['_id']
            records[item] = renter
    return records


'''
show_rentals(product_id): 

Returns a Python dictionary with the following user information from
users that have rented products matching product_id:

user_id.
name.
address.
phone_number.
email.

For example:

{‘user001’:{‘name’:’Elisa Miles’,
    ’address’:‘4490 Union Street’,
    ’phone_number’:‘206-922-0882’,
    ’email’:’elisa.miles@yahoo.com’},
    ’user002’:{‘name’:’Maya Data’,
    ’address’:‘4936 Elliot Avenue’,
    ’phone_number’:‘206-777-1927’,
    ’email’:’mdata@uw.edu’}
}
'''
