#!/usr/bin/env python3

'''Functions to add and remove items from furniture mongoDB'''

# Rachel Schirra
# May 4, 2019
# Python 220 Lesson 05

import csv
from pymongo import MongoClient
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
    errors = {'customer': 0,
              'product': 0,
              'rentals': 0}

    path = '{directory}\\{file}'

    logger.debug('Converting products file to dictionary')
    product_dict = import_csv(path.format(
        directory=directory_name,
        file=product_file
        ))

    logger.debug('Converting customers file to dictionary')
    customer_dict = import_csv(path.format(
        directory=directory_name,
        file=customer_file
        ))

    logger.debug('Converting rentals file to dictionary')
    rentals_dict = import_csv(path.format(
        directory=directory_name,
        file=rentals_file
        ))

    mongo = MongoDBConnection()
    logger.debug('Connecting to MongoDB')
    with mongo:
        logger.debug('Connecting to hpnorton database')
        db = mongo.connection.hpnorton
        logger.debug('Creating customer table')
        custs = db['customer']
        logger.debug('Inserting data to customer table')
        result = custs.insert_many(customer_dict)
        records['customer'] = len(result.inserted_ids)

        logger.debug('Creating product table')
        prods = db['product']
        logger.debug('Inserting data to product table')
        result = prods.insert_many(product_dict)

        logger.debug('Creating rentals table')
        rents = db['rentals']
        logger.debug('Inserting data to rentals table')
        result = rents.insert_many(rentals_dict)


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
