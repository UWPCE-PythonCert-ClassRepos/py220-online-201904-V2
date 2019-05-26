# pylint: disable = W0703, C0301
""" the MongoDB Database"""

import csv
import os
import pathlib
import logging
import time
import multiprocessing
import pprint
from itertools import starmap
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMMATER = logging.Formatter(LOG_FORMAT)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMMATER)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)


class MongoDBConnection:
    """ Make the database connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


CLIENT = MongoDBConnection()
DIRECTORY_NAME = pathlib.Path(os.path.abspath(__file__)).parents[1] / "data"
PRODUCT_FILE = "product.csv"
CUSTOMER_FILE = "customer.csv"
RENTAL_FILE = "rental.csv"
PRODUCT_FILE_PATH = os.path.join(DIRECTORY_NAME, PRODUCT_FILE)
CUSTOMER_FILE_PATH = os.path.join(DIRECTORY_NAME, CUSTOMER_FILE)
RENTAL_FILE_PATH = os.path.join(DIRECTORY_NAME, RENTAL_FILE)
COLLECTIONS = ["product", "customer", "rental"]
FILE_PATH = [PRODUCT_FILE_PATH, CUSTOMER_FILE_PATH, RENTAL_FILE_PATH]


def read_file(file, collection_name):
    """ open csv file and return the data in dictionary structure"""
    try:
        file_handler = open(file, newline='')
        rows = csv.reader(file_handler)
        header = next(rows)
        # remove the weird prefix created for the first item in header
        if header[0].startswith("ï»¿"):
            header[0] = header[0][3:]
        row = csv.DictReader(file_handler, fieldnames=header)
        return write_to_collection(collection_name, row)
    except Exception:
        LOGGER.warning("There is issue with the your file!")


def write_to_collection(collection_name, data):
    """ write data which is dictionary type into the collection"""
    try:
        with CLIENT:
            hp_norton_db = CLIENT.connection.hpnorton
            # collection in database
            collection = hp_norton_db[collection_name]
            collection_count_before_running = collection.count_documents({})
            collection.insert_many(data)
            collection_count_after_running = collection.count_documents({})
            process_count = collection_count_after_running - collection_count_before_running
            return process_count, collection_count_before_running, collection_count_after_running
    except Exception:
        LOGGER.warning("There is an issue in database connection ")


def linear():
    """ import data to database linear """
    start_time = time.perf_counter()
    result = starmap(read_file, zip(FILE_PATH, COLLECTIONS))
    end_time = time.perf_counter()
    performance_time = end_time - start_time
    return tuple(zip(*zip(*result), (performance_time, performance_time, performance_time)))


def parallel():
    """ import data to database parallel"""
    start_time = time.perf_counter()
    with multiprocessing.Pool(processes=4) as pool:
        result = pool.starmap(read_file, zip(FILE_PATH, COLLECTIONS))
        end_time = time.perf_counter()
        performance_time = end_time - start_time
        return tuple(zip(*zip(*result), (performance_time, performance_time, performance_time)))


def print_mdb_collection(collection_name):
    '''
    Prints the documents in columns.  May address this later, may not
    '''
    for doc in collection_name.find():
        pprint.pprint(doc)


def show_available_products():
    """ return the available product"""
    with CLIENT:
        # mongodb database;
        hp_norton_db = CLIENT.connection.hpnorton
        query = {'quantity_available': {'$gt': '1'}}  # item with quantity more or equal to 1
        result = hp_norton_db.products.find(query, {'_id': 0})
        # make the return result as per assignment a dictionary of available products
        available_product = {}
        for doc in result:
            available_product.update({list(doc.values())[0]: dict(list(doc.items())[1:])})
        return available_product


def show_rentals(product_id):
    """ return the customers that rent specific product"""
    with CLIENT:
        # mongodb database;
        hp_norton_db = CLIENT.connection.hpnorton
        result = hp_norton_db.rentals.find({'product_id': product_id})
        rental_users = {}
        for user in result:
            doc = hp_norton_db.customers.find_one({'user_id': user['user_id']}, {'_id': 0})
            rental_users.update({list(doc.values())[0]: dict(list(doc.items())[1:])})
        return rental_users


def drop_collection(collection):
    """ drop the collection"""
    with CLIENT:
        # mongodb database;
        hp_norton_db = CLIENT.connection.hpnorton
        for collec in collection:
            hp_norton_db.drop_collection(collec)


if __name__ == "__main__":
    print(list(linear()))
    # drop_collection(collections)
    # print(list(parallel()))
    # drop_collection(collections)
