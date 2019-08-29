"""
This module utilizes MongoDB to build a product database for
HP Norton.
"""
import gc
import json
from pathlib import Path
import time
from loguru import logger
import pandas as pd
from pymongo import MongoClient

MONGO = MongoClient("mongodb://localhost:27017/")

logger.add("100K_Record_Log.log")


def open_DB():
    try:
        DB = MONGO["HP_Norton"]
        return DB
    except Exception as e:
        print(f"Error {e} encountered")


DB = open_DB()


def view_collections():
    """
    Function that return existing collections.
    :return: Collection names.
    """
    collections_list = []
    for i in DB.list_collection_names():
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
        remove = DB[name]
        remove.drop()


def import_data(*args):
    """
    Imports csv files, creates jsons with the csv file data, then
    creates collections with the jsons. Args are user supplied
    :param args: data source path, customer, product, and rental
    data source names
    :return: collections with same name as data sources
    """
    logger.info("Importing 100K records")
    DATA_PATH = Path(args[0])
    colls = [i for i in args[1:]]
    remove_a_collection()
    for arg in colls:
        src_csv = DATA_PATH / arg
        src_json = str(DATA_PATH / arg).replace(".csv", ".json")
        coll_csv = pd.read_csv(src_csv, encoding="ISO-8859-1")
        coll_csv.to_json(src_json, orient="records")
        coll_json = open(src_json).read()
        coll_json = json.loads(coll_json)

        coll = DB[arg[:-4]]
        source = coll_json
        coll.insert_many(source)
    DB.product.create_index("product_id", unique=True)
    DB.customers.create_index("user_id", unique=True)
    prod_count = DB.product.count_documents({})
    customer_count = DB.customers.count_documents({})
    rental_count = DB.rental.count_documents({})
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
    logger.info(f"Process time was {time.process_time()}:")
    return count, errors


def show_available_products():
    """
    Returns items based on quantity available >0
    :return: listing of available rentals
    """
    return_fields = {
        "_id": False,
        "product_id": True,
        "description": True,
        "product_type": True,
        "quantity_available": True,
    }
    available = [
        i
        for i in DB.product.find(
            {"quantity_available": {"$ne": 0}}, projection=return_fields
        )
    ]
    return available


def get_all_product_ids():
    """
    creates list of product ids
    :return: list
    """
    product_id_list = []
    products = DB.product.find()
    for prod_id in products:
        product_id_list.append(prod_id["product_id"])
    return product_id_list


def get_rental_user_id(product_id):
    """
    returns a set of user_id's of customers who have rented
    a specific product
    :param product_id:
    :return: set of user_id's
    """
    user_id_set = set()
    renters = DB.rental.find({"product_id": product_id})
    for item in renters:
        user_id_set.add(item["user_id"])
    return user_id_set


def show_rentals(product_id):
    """
    returns customers who have rented specific products
    :param product_id:
    :return: dictionary of renters
    """
    return_fields = {
        "_id": False,
        "user_id": True,
        "name": True,
        "address": True,
        "phone_number": True,
        "email": True,
    }
    if product_id in get_all_product_ids():
        for i in get_rental_user_id(product_id):
            renters = DB.customers.find({"user_id": i}, projection=return_fields)
            for renter in renters:
                return renter
    else:
        print("Invalid product code")


if __name__ == "__main__":

    def run():
        """
        Simple script runner for on the fly testing
        :return: funtions called
        """
        remove_a_collection()
        src_path = Path.cwd().with_name("data")
        print(import_data(src_path, "product.csv", "customer_large.csv", "rental.csv"))
        print(show_available_products())
        print(show_rentals("prd001"))

    run()
    gc.collect()
