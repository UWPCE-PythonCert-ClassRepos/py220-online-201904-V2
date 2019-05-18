"""
This module utilizes MongoDB to build a product database for
HP Norton.
"""
import gc
import json
from pathlib import Path
import threading
import time
from loguru import logger
import os
from pymongo import MongoClient
import pandas as pd
from decorator import timer

mongo = MongoClient("mongodb://localhost:27017/")
db = mongo['HP_Norton']

DATA_PATH = Path.cwd().with_name('data')
PROCESS_RESULT = []

logger.add('Parallel Log.log')


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
        logger.info(f"Removing collection: {name}:")
        remove = db[name]
        remove.drop()


def _delete_json():
    """
    Clearun utility that deletes json files created in
    collection creation process.
    :return:
    """
    os.chdir(DATA_PATH)
    removal_path = Path.cwd()
    for json in removal_path.iterdir():
        if json.suffix == '.json':
            logger.info(f'Removing {json.name}.')
            os.remove(json.name)


@logger.catch()
def _read_data_create_collection(data):
    """
    Imports csv files, creates jsons with the csv file data, then
    creates collections with the jsons. Args are user supplied
    :param args: data source path, customer, product, and rental
    data source names
    :return: collections with same name as data sources
    """
    src_csv = DATA_PATH / data
    src_json = str(DATA_PATH / data).replace(".csv", '.json')
    logger.info(f"Reading csv: {data}:")
    coll_csv = pd.read_csv(src_csv, encoding='ISO-8859-1')
    len_csv = int(coll_csv.iloc[:, 0].count())
    coll_csv.to_json(src_json,
                     orient='records')
    logger.info(f"Opening json: {src_json}:")
    coll_json = open(src_json).read()
    coll_json = json.loads(coll_json)
    coll = db[data[:-4]]
    source = coll_json
    start_count = coll.count_documents({})
    logger.info(f"Inserting data into : {coll}:")
    result = coll.insert_many(source)
    gc.collect()
    record_count = coll.count_documents({})
    result_tuple = (len_csv, start_count, record_count, time.thread_time())
    logger.info(f"Process time was {time.thread_time()}:")
    PROCESS_RESULT.append(result_tuple)


@timer
def import_data_threading():
    """
    Runs _read_data_create_collection through threading"""

    colls = ('product.csv', 'customers.csv')

    threads = [threading.Thread(target=_read_data_create_collection,
                                args=(colls[0],)),
               threading.Thread(target=_read_data_create_collection,
                                args=(colls[1],))]

    for t in threads:
        logger.info(f"Starting thread {t}:")
        t.start()

    for t in threads:
        logger.info(f"Joining thread {t}:")
        t.join()

    return PROCESS_RESULT


@timer
def import_data_queue():
    """
    Runs _read_data_create_collection via a queue"""

    colls = ('product.csv', 'customers.csv')

    for col in colls:
        worker = threading.Thread(target=_read_data_create_collection,
                                  args=(col,))
        worker.daemon = True
        worker.start()
        worker.join()


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


def get_rental_user_id(product_id: str) -> str:
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


def show_rentals(product_id: str) -> str:
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
    def run():
        """
        Simple script runner for on the fly testing
        :return: funtions called
        """
        remove_a_collection()
        print(import_data_threading())
        _delete_json()


    run()
    gc.collect()
