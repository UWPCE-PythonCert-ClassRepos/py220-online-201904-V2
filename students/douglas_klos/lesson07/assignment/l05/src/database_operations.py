#!/usr/bin/env python3
#pylint: disable=eval-used
""" HPNorton API for accessing MongoDB collections """

from os import path
from multiprocessing import Process, Queue
from time import time
import pymongo
from loguru import logger
import src.mongodb_conn as mdb_conn
from src.settings import Settings

MONGO = mdb_conn.MongoDBConnection()


def linear(files):
    """ Import csv files into mongodatabase.

    Arguments:
        directory_name {string} -- directory data files are stored in
        *files {list} -- *args list of csv files to import

    Returns:
        ((),()) -- Tuple of Tuples, ((Success),(Failures)) from imports
    """

    return list(map(insert_to_mongo, files))


def parallel(files):
    """ Import csv files into mongodatabase.

    Arguments:
        files {list} -- args list of csv files to import

    Returns:
        {{},{},,} -- {csv_file: {elapsed, fail, success, total_records},}

    """

    return list(map(join_process, list(map(start_process, files))))


def start_process(csv_file):
    """Start process on given csv_file

    Arguments:
        csv_file {string} -- csv_file to start insert process on

    Returns:
        process, Queue -- process started, Queue with dict of results
    """
    results = Queue()
    process = Process(target=insert_to_mongo, args=(csv_file, results))
    logger.info(f"Starting {process} : {csv_file}")
    process.start()
    return process, results


def join_process(process):
    """Joins processes in process argument

    Arguments:
        process {list} -- list of processes to join

    Returns:
        dict -- Results from join
    """
    logger.info(f"Joining process {process[0]}")
    process[0].join()
    return process[1].get()


# pylint: disable=R0914
def insert_to_mongo(filename, results=None):
    """ Inserts given csv file into mongo

    Arguments:
        directory_name {string} -- directory containing csv file
        filename {string} -- csv filename to import

    Returns:

    """
    success = 0
    fail = 0
    start = time()
    collection_name, _ = path.splitext(path.basename(filename))

    with MONGO:
        mdb = eval(Settings.connect_string)
        logger.info(f"Inserting {collection_name} into Mongo...")
        collection = mdb[collection_name]
        iter_lines = get_line(open_file(filename))
        header = next(iter_lines).split(",")

        # Create the indicies for the collection
        if collection.name[:6] != "rental":
            logger.info("rental collection")
            collection.create_index(header[0], unique=True)
        else:
            logger.info("creating rental index")
            collection.create_index(
                [
                    (header[0], pymongo.ASCENDING),
                    (header[5], pymongo.ASCENDING),
                ],
                unique=True,
            )

        # Iterate through lines and insert records
        for line in iter_lines:
            line = line.split(",")
            new_addition = {}
            for num, field in enumerate(header):
                new_addition[field] = line[num]
            try:
                collection.insert_one(new_addition)
                success += 1
            except pymongo.errors.DuplicateKeyError:
                fail += 1

    # This allows us to use the same insert function
    #   for both linear and parallel inserts.
    return_dict = {
        collection_name: {
            "success": success,
            "fail": fail,
            "total_records": collection.count_documents({}),
            "elapsed": time() - start,
        }
    }

    # We get AttributeError for None.put() if in linear since we
    #   don't pass in a queue object.
    try:
        results.put(return_dict)
        return 0
    except AttributeError:
        return return_dict


def show_available_products():
    """ Creates a list of currently available products

    Returns:
        dict -- Dictionary of Mongo documents, key=product_id
    """
    logger.info(f"Preparing dict of available prodcuts...")
    available_products = {}

    with MONGO:
        mdb = eval(Settings.connect_string)
        products = mdb["product"]
        for doc in products.find():
            del doc["_id"]
            if int(doc["quantity_available"]) > 0:
                product_id = doc["product_id"]
                del doc["product_id"]
                available_products[product_id] = doc

    return available_products


def list_all_products():
    """ Prepares a dictionary of all products

    Returns:
        dict -- Dictionary containing all products
    """
    logger.info(f"Perparing dict of all products...")
    all_products_dict = {}

    with MONGO:
        mdb = eval(Settings.connect_string)
        products = mdb["product"]
        all_products = products.find({})
        for product in all_products:
            product_id = product["product_id"]
            del product["_id"]
            del product["product_id"]
            all_products_dict[product_id] = product
    return all_products_dict


def list_all_rentals():
    """ Prepares a dictionary of all products

    Returns:
        dict -- Dictionary containing all products
    """
    logger.info(f"Perparing dict of all products...")
    all_rentals_dict = {}

    with MONGO:
        mdb = eval(Settings.connect_string)
        rentals = mdb["rental"]
        all_rentals = rentals.find({})
        for rental in all_rentals:
            customer_id = rental["user_id"]
            del rental["_id"]
            del rental["user_id"]
            all_rentals_dict[customer_id] = rental
    return all_rentals_dict


def list_all_customers():
    """ Prepares a dictionary of all customers

    Returns:
        dict -- Dictionary containing all customers
    """
    logger.info(f"Perparing dict of all products...")
    all_customers_dict = {}

    with MONGO:
        mdb = eval(Settings.connect_string)
        customers = mdb["customers"]
        all_customers = customers.find({})
        for customer in all_customers:
            user_id = customer["user_id"]
            del customer["_id"]
            del customer["user_id"]
            all_customers_dict[user_id] = customer
    return all_customers_dict


def rentals_for_customer(user_id):
    """Prepares a dict of products rented by user_id

    Arguments:
        user_id {string} -- user_id reference into product collection

    Returns:
        dict -- Dictionary of products rented by specified user_id
    """
    logger.info(f"Perparing customer dict for user_id: {user_id}...")
    rentals_for_user = []

    with MONGO:
        mdb = eval(Settings.connect_string)

        rentals = mdb["rental"]
        products = mdb["product"]
        query = {"user_id": user_id}

        # First we get a list of rentals for the specified user_id
        for rental in rentals.find(query):
            # Now we get product details from products via the product_id
            query = {"product_id": rental["product_id"]}

            for product in products.find(query):
                del product["_id"]
                del product["quantity_available"]
                rentals_for_user.append(product)

    return rentals_for_user


def customers_renting_product(product_id):
    """Prepares a dict of customers renting product_id

    Arguments:
        product_id {string} -- product_id reference into rental collection

    Returns:
        dict -- Dictionary of rental customers for specified product_id
    """
    logger.info(f"Perparing rental dict for product_id: {product_id}...")
    users_renting_product = []

    with MONGO:
        mdb = eval(Settings.connect_string)

        rentals = mdb["rental"]
        customers = mdb["customers"]
        query = {"product_id": product_id}

        # First we get a list of customers for the specified product_id
        for rental in rentals.find(query):
            # Now we get customer details from customers via user_id
            query = {"user_id": rental["user_id"]}
            logger.info(rental["user_id"])

            for customer in customers.find(query):
                logger.info(customer)
                del customer["_id"]
                users_renting_product.append(customer)

    return users_renting_product


def get_line(lines):
    """ Generator for lines of content from csv file

    Arguments:
        lines {list} -- List of lines containing data from csv file

    Yields:
        string -- CSV string containing information for a single customer.
    """
    for line in lines:
        yield line


def open_file(filename):
    """ Opens the file specified from the command line

    Arguments:
        filename {string} -- Name of CSV file to import

    Returns:
        list containing lines of customer data from csv file
    """
    with open(filename, "rb") as content:
        return content.read().decode("utf-8", errors="ignore").split("\n")


def drop_database():
    """ Drops database """

    logger.warning(f"Dropping {Settings.database_name} database")
    mdb = mdb_conn.MongoClient()
    mdb.drop_database(Settings.database_name)


def drop_collections():
    """ Drops collections from Mongo that are used for this program """

    with MONGO:
        mdb = eval(Settings.connect_string)
        logger.info(mdb.list_collection_names())
        collections = list(
            filter(lambda x: x != "system.indexes", mdb.list_collection_names())
        )
        for collection in collections:
            logger.info(f"Dropping {collection}...")
            mdb.drop_collection(collection)

    logger.warning("Purge complete!")
