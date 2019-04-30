"""
This module utilizes MongoDB to build a product database for
HP Norton.
"""
import csv
import json
import pandas as pd
from pathlib import Path
from pymongo import MongoClient
import pysnooper

CUST_SRC_PATH = Path.cwd().with_name('data') / 'customers.csv'
PROD_SRC_PATH = Path.cwd().with_name('data') / 'product.csv'
RENT_SRC_PATH = Path.cwd().with_name('data') / 'rental.csv'


class MongoDBConnection():
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


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)


def read_in_data(path, file_name):
    """
    Reads in csv and converts the data to json file.
    :param file_name:
    :return: json file
    """
    customer_csv = pd.read_csv(path, encoding='ISO-8859-1')
    customer_csv.to_json(Path.cwd().with_name('data') / file_name)
    cust_json = open(Path.cwd().with_name('data') / file_name).read()
    cust_json = json.loads(cust_json)
    return cust_json


def create_collection(database, coll_name, sp, fn):
    """
    Function to create a collection"""
    coll = database[coll_name]
    source = read_in_data(sp, fn)
    coll.insert_one(source)
    return coll

def remove_a_collection(database, collection_name):
    remove = database[collection_name]
    remove.drop()


def main():
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        def view_collections():
            """
            Function that return existing collections.
            :return: Collection names.
            """
            for i in db.list_collection_names():
                print(i)

        def create_customers():
            """
            Function to create the customers collection"""
            customers = create_collection(db, "customers", CUST_SRC_PATH, 'customers.json')
            return customers

        def create_products():
            """
            Function to create the products collection
            :return: products collection
            """
            products = create_collection(db, "products", PROD_SRC_PATH, 'products.json')
            return products

        def create_rentals():
            """
            Function to create rentals collection
            :return: rentals collection
            """
            rentals = create_collection(db, "rentals", PROD_SRC_PATH, 'rentals.json')
            return rentals

        def dictionary_switch(selection):
            functions = {'customers': create_customers,
                         'products': create_products,
                         'rentals': create_rentals}
            functions[selection]()

        def show_available_products():
            """
            Returns items based on quantity available >0
            :return:
            """
            available = db.products.find({"quantity_available":{"$ne":0}})
            for item in available:
                print(item)



        show_available_products()

        def create_collections_switch():
            """
            This function checks if a collection exists. If it does it removes it and
            creates a new one.
            :return: New collections
            """
            collections_list = {'customers', 'products', 'rentals'}

            for item in collections_list:
                if item in db.list_collection_names():
                    remove_a_collection(db, item)
                    dictionary_switch(item)
                else:
                    dictionary_switch(item)

        def decisions():
            """
            Function that collects user input and runs functions related to
            that input
            """
            add_new_collections = input("Do you want to add collections?")
            if add_new_collections.upper() == 'Y':
                create_collections_switch()

            view_colls = input("Do you want to see database collections?")
            if view_colls.upper() == "Y":
                view_collections()

        decisions()

if __name__ == "__main__":
    main()
