# pylint: disable = W0703
""" the MongoDB Database"""
import csv
import os
import pprint
from pymongo import MongoClient


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


def print_mdb_collection(collection_name):
    '''
    Prints the documents in columns.  May address this later, may not
    '''
    for doc in collection_name.find():
        pprint.pprint(doc)


def import_data(directory_name, product_file, customer_file, rentals_file):
    """ import data from csv file to database"""
    product_file_path = os.path.join(directory_name, product_file)
    customer_file_path = os.path.join(directory_name, customer_file)
    rentals_file_path = os.path.join(directory_name, rentals_file)
    client = MongoDBConnection()
    with client:
        # mongodb database;
        hp_norton_db = client.connection.hpnorton
        # collection in database
        products = hp_norton_db["products"]
        customers = hp_norton_db["customers"]
        rentals = hp_norton_db["rentals"]
        # delete all data in collection that we can check the code in several tests
        products.delete_many({})
        customers.delete_many({})
        rentals.delete_many({})
        # write data in collections
        product_result = write_to_collection(product_file_path, products)
        customer_result = write_to_collection(customer_file_path, customers)
        rental_result = write_to_collection(rentals_file_path, rentals)
        return tuple(zip(product_result, customer_result, rental_result))


def write_to_collection(file_name, collection):
    """ write document into the collection"""
    try:
        file_handler = open(file_name, newline='')
        rows = csv.reader(file_handler)
        header = next(rows)
        # remove the weird prefix created for the first item in header
        if header[0].startswith("ï»¿"):
            header[0] = header[0][3:]
        row = csv.DictReader(file_handler, fieldnames=header)
        collection.insert_many(row)
        collection_count = collection.count_documents({})
        return collection_count, 0
    except Exception:
        return 0, 1
    finally:
        file_handler.close()


def show_available_products():
    """ return the available product"""
    client = MongoDBConnection()
    with client:
        # mongodb database;
        hp_norton_db = client.connection.hpnorton
        query = {'quantity_available': {'$gt': '1'}}  # item with quantity more or equal to 1
        result = hp_norton_db.products.find(query, {'_id': 0})
        # make the return result as per assignment a dictionary of available products
        available_product = {}
        for doc in result:
            available_product.update({list(doc.values())[0]: dict(list(doc.items())[1:])})
        # pprint.pprint(available_product)
        return available_product


def show_rentals(product_id):
    """ return the customers that rent specific product"""
    client = MongoDBConnection()
    with client:
        # mongodb database;
        hp_norton_db = client.connection.hpnorton
        result = hp_norton_db.rentals.find({'product_id': product_id})
        rental_users = {}
        for user in result:
            doc = hp_norton_db.customers.find_one({'user_id': user['user_id']}, {'_id': 0})
            rental_users.update({list(doc.values())[0]: dict(list(doc.items())[1:])})
        # pprint.pprint(rental_users)
        return rental_users
