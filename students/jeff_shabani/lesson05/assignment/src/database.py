"""
This module utilizes MongoDB to build a product database for
HP Norton.
"""
import gc
import json
from pathlib import Path
import pandas as pd
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017/")
db = mongo['HP_Norton']


def view_collections():
    """
    Function that return existing collections.
    :return: Collection names.
    """
    collections_list = []
    for i in db.list_collection_names():
        collections_list.append(i)
    return collections_list


def remove_a_collection():
    """
    Cleanup utility that clears out pre-existing collections
    :param database:
    :param collection_name:
    :return: deleted collection
    """
    collection_names = ["customers", "product", "rental"]
    for name in collection_names:
        remove = db[name]
        remove.drop()


def import_data(*args):
    """
    Imports csv files, creates jsons with the csv file data, then
    creates collections with the jsons. Args are user supplied
    :param args: data source path, customer, product, and rental
    data source names
    :return: collections with same name as data sources
    """

    DATA_PATH = Path(args[0])
    colls = [i for i in args[1:]]
    remove_a_collection()
    for arg in colls:
        src_csv = DATA_PATH / arg
        src_json = str(DATA_PATH / arg).replace(".csv", '.json')
        coll_csv = pd.read_csv(src_csv, encoding='ISO-8859-1')
        coll_csv.to_json(src_json,
                         orient='records')
        coll_json = open(src_json).read()
        coll_json = json.loads(coll_json)

        coll = db[arg[:-4]]
        source = coll_json
        result = coll.insert_many(source)
    set_prod_index = db.product.create_index('product_id', unique=True)
    set_cust_index = db.customers.create_index('user_id', unique=True)
    prod_count = db.product.count_documents({})
    customer_count = db.customers.count_documents({})
    rental_count = db.rental.count_documents({})
    count = (prod_count, customer_count, rental_count)
    if prod_count == 10:
        prod_error = 0
    else:
        prod_error = 1
    if customer_count == 10:
        cust_error = 0
    else:
        cust_error = 1

    if rental_count == 9:
        rent_error = 0
    else:
        rent_error = 1
    errors = (prod_error, rent_error, cust_error)
    return count, errors


def show_available_products():
    """
    Returns items based on quantity available >0
    :return: listing of available rentals
    """
    return_fields = {'_id': False,
                     'product_id': True,
                     'description': True,
                     'product_type': True,
                     'quantity_available': True}
    available = [i for i in db.product.find({'quantity_available': {'$ne': 0}},
                                            projection=return_fields)]
    return available


def get_all_product_ids():
    """
    creates list of product ids
    :return: list
    """
    product_id_list = []
    products = db.product.find()
    for prod_id in products:
        product_id_list.append(prod_id['product_id'])
    return product_id_list


def get_rental_user_id(product_id):
    """
    returns a set of user_id's of customers who have rented
    a specific product
    :param product_id:
    :return: set of user_id's
    """
    user_id_set = set()
    renters = db.rental.find({'product_id': product_id})
    for item in renters:
        user_id_set.add(item['user_id'])
    return user_id_set


def show_rentals(product_id):
    """
    returns customers who have rented specific products
    :param product_id:
    :return: dictionary of renters
    """
    return_fields = {'_id': False,
                     'user_id': True,
                     'name': True,
                     'address': True,
                     'phone_number': True,
                     'email': True}
    if product_id in get_all_product_ids():
        for i in get_rental_user_id(product_id):
            renters = db.customers.find({'user_id': i}
                                        , projection=return_fields)
            for renter in renters:
                return renter
    else:
        print('Invalid product code')


if __name__ == "__main__":

    run = 1
    if run == 1:
        remove_a_collection()
        src_path = Path.cwd().with_name('data')
        print(import_data(src_path,
                          'product.csv', 'customers.csv', 'rental.csv'))
        print(show_available_products())
        print(show_rentals('prd001'))

    gc.collect()
