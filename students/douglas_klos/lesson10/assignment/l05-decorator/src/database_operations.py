#!/usr/bin/env python3
# pylint: disable=W0613
""" HPNorton API for accessing MongoDB collections """

from datetime import datetime
from multiprocessing import Process, Queue
from os.path import splitext, basename
from time import time
from wrapt import decorator
from loguru import logger
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
import src.mongodb_conn as mdb_conn


MONGO = mdb_conn.MongoDBConnection()


@decorator
def timer_logger(function, instance, args, kwargs):
    """ Times functions and writes results to timings.txt """
    start = datetime.now()
    result = function(*args, **kwargs)
    end = datetime.now()
    with open("timings.txt", "a") as log_file:
        log_file.write(
            f"{function.__name__} "
            f"called at {start.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        if (
                function.__name__ == "insert_to_mongo" or
                function.__name__ == "get_line_from_file"
        ):
            record_count = 0
            for _ in open(args[0]):
                record_count += 1
            log_file.write(f"\tCalled on {record_count} records\n")
        else:
            log_file.write(f"\targs:{args}, kwargs:{kwargs}\n")
        log_file.write(f"\tExecution time {end - start} seconds\n")
    return result


@timer_logger
def linear(files):
    """ Import csv files into mongodatabase.

    Arguments:
        [file1, file2, file3, ...] -- list of files to import

    Returns:
        {{},{},,} -- {csv_file: {elapsed, fail, success, total_records},}
    """
    return list(map(insert_to_mongo, files))


@timer_logger
def parallel(files):
    """ Import csv files into mongodatabase.

    Arguments:
        [file1, file2, file3, ...] -- list of files to import

    Returns:
        {{},{},,} -- {csv_file: {elapsed, fail, success, total_records},}

    """
    return list(map(join_process, list(map(start_process, files))))


@timer_logger
def start_process(csv_file):
    """ Start process on given csv_file

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


@timer_logger
def join_process(process):
    """ Joins processes in process argument

    Arguments:
        [process1, process2, process3, ...] -- list of processes to join

    Returns:
        {collection_name: {"success", "fail", "total_records", "elapsed"}}
    """
    logger.info(f"Joining process {process[0]}")
    process[0].join()
    return process[1].get()


# pylint: disable=R0914
@timer_logger
def insert_to_mongo(filename, results=None):
    """ Inserts given csv file into mongo

    Arguments:
        filename {string} -- csv filename to import

    Returns:
        {collection_name: {"success", "fail", "total_records", "elapsed"}}
    """
    success = 0
    fail = 0
    start = time()
    collection_name, _ = splitext(basename(filename))

    with MONGO as mdb:
        logger.info(f"Inserting {collection_name} into Mongo...")
        collection = mdb[collection_name]
        iter_lines = get_line_from_file(filename)
        header = next(iter_lines).split(",")

        # Create the indicies for the collection
        if collection.name[:6] != "rental":
            collection.create_index(header[0], unique=True)
        else:
            collection.create_index(
                [(header[0], ASCENDING), (header[5], ASCENDING)], unique=True
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
            except DuplicateKeyError:
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


@timer_logger
def show_available_products():
    """ Creates a list of currently available products

    Returns:
        {product_id: {"description", "product_type", "quantity_available"}}
    """
    logger.info(f"Preparing dict of available prodcuts...")
    available_products = {}

    with MONGO as mdb:
        products = mdb["product"]
        for doc in products.find():
            del doc["_id"]
            if int(doc["quantity_available"]) > 0:
                product_id = doc["product_id"]
                del doc["product_id"]
                available_products[product_id] = doc

    return available_products


@timer_logger
def list_all_products():
    """ Prepares a dictionary of all products

    Returns:
        {product_id: {"description", "product_type", "quantity_available"}}
    """
    logger.info(f"Perparing dict of all products...")
    all_products_dict = {}

    with MONGO as mdb:
        products = mdb["product"]
        all_products = products.find({})
        for product in all_products:
            product_id = product["product_id"]
            del product["_id"]
            del product["product_id"]
            all_products_dict[product_id] = product
    return all_products_dict


@timer_logger
def list_all_rentals():
    """ Prepares a dictionary of all rentals

    Returns:
        {user_id: {"address", "email", "name", "phone_number", "product_id"}}
    """
    logger.info(f"Perparing dict of all rentals...")
    all_rentals_dict = {}

    with MONGO as mdb:
        rentals = mdb["rental"]
        all_rentals = rentals.find({})
        for rental in all_rentals:
            customer_id = rental["user_id"]
            del rental["_id"]
            del rental["user_id"]
            all_rentals_dict[customer_id] = rental
    return all_rentals_dict


@timer_logger
def list_all_customers():
    """ Prepares a dictionary of all customers

    Returns:
        {user_id: {"credit_limit",
                   "email_address",
                   "home_address",
                   "last_name",
                   "name",
                   "phone_number",
                   "status"}}
    """
    logger.info(f"Perparing dict of all customers...")
    all_customers_dict = {}

    with MONGO as mdb:
        customers = mdb["customers"]
        all_customers = customers.find({})
        for customer in all_customers:
            user_id = customer["user_id"]
            del customer["_id"]
            del customer["user_id"]
            all_customers_dict[user_id] = customer
    return all_customers_dict


@timer_logger
def rentals_for_customer(user_id):
    """Prepares a dict of products rented by user_id

    Arguments:
        user_id {string} -- user_id reference into product collection

    Returns:
        [{"description", "product_id", "product_type"}, {...}, ...]
    """
    logger.info(f"Perparing customer dict for user_id: {user_id}...")
    rentals_for_user = []

    with MONGO as mdb:
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


@timer_logger
def customers_renting_product(product_id):
    """Prepares a dict of customers renting product_id

    Arguments:
        product_id {string} -- product_id reference into rental collection

    Returns:
        [{"credit_limit",
          "email_address",
          "last_name",
          "name",
          "phone_number",
          "status",
          "user_id"}, {...}, ...]
    """
    logger.info(f"Perparing rental dict for product_id: {product_id}...")
    users_renting_product = []

    with MONGO as mdb:

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


@timer_logger
def get_line_from_file(filename):
    """ Opens the file specified from the command line

    Arguments:
        filename {string} -- Name of CSV file to import

    Returns:
        list containing lines of customer data from csv file
    """
    with open(filename, "rb") as content:
        lines = content.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines:
            yield line


@timer_logger
def drop_database():
    """ Drops database """

    logger.warning(f"Dropping {MONGO.database_name} database")
    mdb = mdb_conn.MongoClient()
    mdb.drop_database(MONGO.database_name)


@timer_logger
def drop_collections():
    """ Drops collections from Mongo that are used for this program """

    with MONGO as mdb:
        logger.info(mdb.list_collection_names())
        collections = list(
            filter(lambda x: x != "system.indexes", mdb.list_collection_names())
        )
        for collection in collections:
            logger.info(f"Dropping {collection}...")
            mdb.drop_collection(collection)

    logger.warning("Purge complete!")
