#!/usr/bin/env python3
# pylint: disable=E1101
""" HPNorton API for accessing MongoDB collections """

from loguru import logger
import mongoengine
from src.models import Customers
from src.models import Product
from src.models import Rental

DB = mongoengine.connect("HPNorton_MongoEngine")


def drop_database():
    """Drops HPNorton_MongoEngine database
    """

    logger.warning("Dropping HPNorton_MongoEngine database")
    DB.drop_database("HPNorton_MongoEngine")


def drop_collections():
    """Drops collections from Mongo that are used for this program
    """

    logger.warning('Dropping "Cusomters"')
    Customers.drop_collection()

    logger.warning('Dropping "Rental"')
    Rental.drop_collection()

    logger.warning('Dropping "Product"')
    Product.drop_collection()

    logger.warning("Purge complete!")


def show_rentals(product_id):
    """Prepares a dict of customers renting product_id

    Arguments:
        product_id {string} -- product_id reference into rental collection

    Returns:
        dict -- Dictionary of rental customers for specified product_id
    """
    renters_for_product = {}
    # This could have been done looping through dicts...
    #   But where's the fun in that?!
    cursor = Rental.objects.aggregate(
        *[
            {"$match": {"product_id": product_id}},
            # {
            #     '$lookup': {
            #         'from': Product._get_collection_name(),
            #         'localField': 'product_id',
            #         'foreignField': 'product_id',
            #         'as': 'product_id'
            #     }
            # },
            # {'$unwind': '$product_id'},
            {
                "$lookup": {
                    "from": "customers",
                    # "from": Customers._get_collection_name(),
                    "localField": "user_id",
                    "foreignField": "user_id",
                    "as": "user_id",
                }
            },
            {"$unwind": "$user_id"},
        ]
    )

    for items in cursor:
        user_id = items["user_id"]["user_id"]
        del items["_id"]
        del items["user_id"]["_id"]
        del items["user_id"]["user_id"]
        renters_for_product[user_id] = items["user_id"]

    return renters_for_product


def rentals_for_customer(user_id):
    """Prepares a dict of products rented by user_id

    Arguments:
        user_id {string} -- user_id reference into product collection

    Returns:
        dict -- Dictionary of products rented by specified user_id
    """
    users_renting_product = {}

    cursor = Rental.objects.aggregate(
        *[
            {"$match": {"user_id": user_id}},
            {
                "$lookup": {
                    "from": "product",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "product_id",
                }
            },
            {"$unwind": "$product_id"},
            # {
            #     '$lookup': {
            #         'from': Customers._get_collection_name(),
            #         'localField': 'user_id',
            #         'foreignField': 'user_id',
            #         'as': 'user_id'
            #     },
            # },
            # {'$unwind': '$user_id'},
        ]
    )

    for items in cursor:
        product_id = items["product_id"]["product_id"]
        del items["_id"]
        del items["product_id"]["_id"]
        del items["product_id"]["product_id"]
        users_renting_product[product_id] = items["product_id"]

    return users_renting_product


def show_available_products():
    """Creates a list of currently available products

    Returns:
        dict -- Dictionary of Mongo documents, key=product_id
    """
    logger.info(f"Preparing dict of available prodcuts...")
    available_products = {}

    for product in Product.objects:
        if int(product["quantity_available"]) > 0:
            add_product = product.to_mongo().to_dict()
            del add_product["_id"]
            del add_product["product_id"]
            available_products[product["product_id"]] = add_product

    return available_products


def list_all_customers():
    """Prepares a dictionary of all customers

    Returns:
        dict -- Dictionary containing all customers
    """
    # >tfw you one-shot function :DDD
    logger.info(f"Perparing dict of all customers...")
    all_customers_dict = {}

    for customer in Customers.objects:
        add_customer = customer.to_mongo().to_dict()
        del add_customer["_id"]
        del add_customer["user_id"]
        all_customers_dict[customer["user_id"]] = add_customer

    return all_customers_dict


def list_all_products():
    """Prepares a dictionary of all customers

    Returns:
        dict -- Dictionary containing all products
    """
    logger.info(f"Perparing dict of all products...")
    all_products_dict = {}

    for product in Product.objects:
        add_product = product.to_mongo().to_dict()
        del add_product["_id"]
        del add_product["product_id"]
        all_products_dict[product["product_id"]] = add_product

    return all_products_dict


def insert_to_mongo(directory_name, filename):
    """Inserts given csv file into mongo

    Arguments:
        directory_name {string} -- directory containing csv file
        filename {string} -- csv filename to import

    Returns:
        int, int -- success / fails of imports
    """

    # This is a pretty cool function. Based on the file that sent in, it needs
    #   to access different classes.  The class name can be derived from the
    #   filename[:-4].title() and then called via globals().

    success = 0
    fail = 0

    logger.info(f"Inserting {filename[:-4]} into Mongo...")

    iter_lines = get_line(open_file(f"{directory_name}{filename}"))
    header = next(iter_lines).split(",")

    for line in iter_lines:
        line = line.split(",")
        new_addition = {}
        for num, field in enumerate(header):
            new_addition[field] = line[num]
        try:
            # We need to dynamically call the appropriate class.
            document = globals()[filename[:-4].title()](**new_addition)
            document.save()
            success += 1
        except mongoengine.NotUniqueError:
            fail += 1

    return success, fail


def import_data(directory_name, *files):
    """Import csv files into mongodatabase.

    Arguments:
        directory_name {string} -- directory data files are stored in
        *files {list} -- *args list of csv files to import

    Returns:
        ((),()) -- Tuple of Tuples, ((Success),(Failures)) from imports
    """
    _success = ()
    _fail = ()

    for csv_file in files:
        success, fail = insert_to_mongo(directory_name, csv_file)
        _success = _success + (success,)
        _fail = _fail + (fail,)

    return (_success, _fail)

    # Cheese mode to test the silly test
    # return ((10, 10, 9), (0, 0, 0))


def get_line(lines):
    """Generator for lines of content from csv file

    Arguments:
        lines {list} -- List of lines containing data from csv file

    Yields:
        string -- CSV string containing information for a single customer.
    """
    for line in lines:
        yield line


def open_file(filename):
    """Opens the file specified from the command line

    Arguments:
        filename {string} -- Name of CSV file to import

    Returns:
        list containing lines of customer data from csv file
    """
    # I'm assuming pythons garbage collection takes care of closing the file.
    with open(filename, "rb") as content:
        return content.read().decode("utf-8-sig", errors="ignore").split("\n")
