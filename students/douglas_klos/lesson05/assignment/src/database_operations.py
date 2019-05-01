#!/usr/bin/env python3

""" HPNorton API for accessing MongoDB collections """

import base64
import pymongo
from loguru import logger
import src.mongodb_conn as mdb_conn

MONGO = mdb_conn.MongoDBConnection()


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


def insert_to_mongo(directory_name, filename):
    """Inserts given csv file into mongo

    Arguments:
        directory_name {string} -- directory containing csv file
        filename {string} -- csv filename to import

    Returns:
        int, int -- success / fails of imports
    """
    success = 0
    fail = 0

    with MONGO:
        mdb = MONGO.connection.media
        logger.info(f"Inserting {filename[:-4]} into Mongo...")
        database_name = mdb[filename[:-4]]

        iter_lines = get_line(open_file(f"{directory_name}{filename}"))
        header = next(iter_lines).split(",")

        if filename[:-4] != "rental":
            database_name.create_index(header[0], unique=True)
        else:
            database_name.create_index(
                [
                    (header[0], pymongo.ASCENDING),
                    (header[1], pymongo.ASCENDING),
                ],
                unique=True,
            )

        for line in iter_lines:
            line = line.split(",")
            new_addition = {}
            for num, field in enumerate(header):
                new_addition[field] = line[num]
            try:
                database_name.insert_one(new_addition)
                success += 1
            except pymongo.errors.DuplicateKeyError:
                fail += 1

    return success, fail


def show_available_products():
    """Creates a list of currently available products

    Returns:
        dict -- Dictionary of Mongo documents, key=product_id
    """
    logger.info(f"Preparing dict of available prodcuts...")
    available_products = {}

    with MONGO:
        mdb = MONGO.connection.media
        products = mdb["product"]
        for doc in products.find():
            del doc["_id"]
            if int(doc["quantity_available"]) > 0:
                product_id = doc["product_id"]
                del doc["product_id"]
                available_products[product_id] = doc

    return available_products


def show_rentals(product_id):
    """Prepares a dict of customers renting product_id

    Arguments:
        product_id {string} -- product_id reference into rental collection

    Returns:
        dict -- Dictionary of rental customers for specified product_id
    """
    logger.info(f"Perparing rental dict for product_id: {product_id}...")
    current_user_rentals = {}

    with MONGO:
        mdb = MONGO.connection.media

        # products = mdb['product']
        rentals = mdb["rental"]
        customers = mdb["customers"]

        # First we get a list of users that have the specified rental
        query = {"product_id": product_id}
        for rental in rentals.find(query):

            # Now we query customers for user_id specified from the rental item.
            query = {"user_id": rental["user_id"]}
            for customer in customers.find(query):
                user_id = customer["user_id"]
                del customer["_id"]
                del customer["user_id"]
                current_user_rentals[user_id] = customer

    return current_user_rentals


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


def drop_databases():
    """Drops collections from Mongo that are used for this program
    """
    logger.warning("Dropping databases, lol!")

    with MONGO:
        mdb = MONGO.connection.media

        customers = mdb['customers']
        logger.warning('Dropping "Cusomters"')
        customers.drop()

        rental = mdb['rental']
        logger.warning('Dropping "Rental"')
        rental.drop()

        product = mdb['product']
        logger.warning('Dropping "Product"')
        product.drop()

    logger.warning("Purge complete!")

    return base64.b64decode('QWxsIHVyIGJhc2UgYXJlIGJlbG9uZyB0byB1cw==')
