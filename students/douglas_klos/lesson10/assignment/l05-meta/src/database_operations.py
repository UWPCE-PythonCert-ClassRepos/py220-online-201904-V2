#!/usr/bin/env python3
""" HPNorton Classes for accessing MongoDB collections """
#pylint: disable=C0103, R0201

from types import MethodType, FunctionType
from datetime import datetime
from multiprocessing import Process, Queue
from os.path import splitext, basename
from time import time
from loguru import logger
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError
import src.mongodb_conn as mdb_conn


def timer_logger(function):
    """ Times functions and writes results to timings.txt """
    def composite(*args, **kwargs):
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
                for _ in open(args[1]):
                    record_count += 1
                log_file.write(f"\tCalled on {record_count} records\n")
            else:
                log_file.write(f"\targs:{args}, kwargs:{kwargs}\n")
            log_file.write(f"\tExecution time {end - start} seconds\n")
        return result

    return composite


class TimerLogger(type):
    """ Metaclass to wrap children with timer_logger function """
    def __new__(cls, name, bases, attr):
        for key, value in attr.items():
            if isinstance(value, (FunctionType, MethodType)):
                attr[key] = timer_logger(value)

        return super(TimerLogger, cls).__new__(cls, name, bases, attr)


class HPNortonDB(metaclass=TimerLogger):
    """ Database operations for HPNorton """

    def __init__(self):
        self.MONGO = mdb_conn.MongoDBConnection()
        super().__init__()

    def linear(self, files):
        """ Import csv files into mongodatabase.

        Arguments:
            [file1, file2, file3, ...] -- list of files to import

        Returns:
            {{},{},,} -- {csv_file: {elapsed, fail, success, total_records},}
        """
        return list(map(self.insert_to_mongo, files))

    def parallel(self, files):
        """ Import csv files into mongodatabase.

        Arguments:
            [file1, file2, file3, ...] -- list of files to import

        Returns:
            {{},{},,} -- {csv_file: {elapsed, fail, success, total_records},}

        """
        return list(
            map(self.join_process, list(map(self.start_process, files)))
        )

    def start_process(self, csv_file):
        """ Start process on given csv_file

        Arguments:
            csv_file {string} -- csv_file to start insert process on

        Returns:
            process, Queue -- process started, Queue with dict of results
        """
        results = Queue()
        process = Process(target=self.insert_to_mongo, args=(csv_file, results))
        logger.info(f"Starting {process} : {csv_file}")
        process.start()
        return process, results

    def join_process(self, process):
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
    def insert_to_mongo(self, filename, results=None):
        """ Inserts given csv file into mongo

        Arguments:
            filename {string} -- csv filename to import
            results {queue} -- Default = None, queue for multiprocessing

        Returns:
            {collection_name: {"success", "fail", "total_records", "elapsed"}}
        """
        success = 0
        fail = 0
        start = time()
        collection_name, _ = splitext(basename(filename))

        with self.MONGO as mdb:
            logger.info(f"Inserting {collection_name} into Mongo...")
            collection = mdb[collection_name]
            iter_lines = self.get_line_from_file(filename)
            header = next(iter_lines).split(",")

            # Create the indicies for the collection
            if collection.name[:6] != "rental":
                collection.create_index(header[0], unique=True)
            else:
                collection.create_index(
                    [(header[0], ASCENDING), (header[5], ASCENDING)],
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

    def show_available_products(self):
        """ Creates a list of currently available products

        Returns:
            {product_id: {"description", "product_type", "quantity_available"}}
        """
        logger.info(f"Preparing dict of available prodcuts...")
        available_products = {}

        with self.MONGO as mdb:
            products = mdb["product"]
            for doc in products.find():
                del doc["_id"]
                if int(doc["quantity_available"]) > 0:
                    product_id = doc["product_id"]
                    del doc["product_id"]
                    available_products[product_id] = doc

        return available_products

    def list_all_products(self):
        """ Prepares a dictionary of all products

        Returns:
            {product_id: {"description", "product_type", "quantity_available"}}
        """
        logger.info(f"Perparing dict of all products...")
        all_products_dict = {}

        with self.MONGO as mdb:
            products = mdb["product"]
            all_products = products.find({})
            for product in all_products:
                product_id = product["product_id"]
                del product["_id"]
                del product["product_id"]
                all_products_dict[product_id] = product
        return all_products_dict

    def list_all_rentals(self):
        """ Prepares a dictionary of all rentals

        Returns:
            {user_id:{"address", "email", "name", "phone_number", "product_id"}}
        """
        logger.info(f"Perparing dict of all rentals...")
        all_rentals_dict = {}

        with self.MONGO as mdb:
            rentals = mdb["rental"]
            all_rentals = rentals.find({})
            for rental in all_rentals:
                customer_id = rental["user_id"]
                del rental["_id"]
                del rental["user_id"]
                all_rentals_dict[customer_id] = rental
        return all_rentals_dict

    def list_all_customers(self):
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

        with self.MONGO as mdb:
            customers = mdb["customers"]
            all_customers = customers.find({})
            for customer in all_customers:
                user_id = customer["user_id"]
                del customer["_id"]
                del customer["user_id"]
                all_customers_dict[user_id] = customer
        return all_customers_dict

    def rentals_for_customer(self, user_id):
        """Prepares a dict of products rented by user_id

        Arguments:
            user_id {string} -- user_id reference into product collection

        Returns:
            [{"description", "product_id", "product_type"}, {...}, ...]
        """
        logger.info(f"Perparing customer dict for user_id: {user_id}...")
        rentals_for_user = []

        with self.MONGO as mdb:
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

    def customers_renting_product(self, product_id):
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

        with self.MONGO as mdb:

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

    def get_line_from_file(self, filename):
        """ Opens the file specified from the command line

        Arguments:
            filename {string} -- Name of CSV file to import

        Yields:
            line from filename
        """
        with open(filename, "rb") as content:
            lines = content.read().decode("utf-8", errors="ignore").split("\n")
            for line in lines:
                yield line

    def drop_database(self):
        """ Drops database """

        logger.warning(f"Dropping {self.MONGO.database_name} database")
        mdb = mdb_conn.MongoClient()
        mdb.drop_database(self.MONGO.database_name)

    def drop_collections(self):
        """ Drops collections from Mongo that are used for this program """

        with self.MONGO as mdb:
            logger.info(mdb.list_collection_names())
            collections = list(
                filter(
                    lambda x: x != "system.indexes", mdb.list_collection_names()
                )
            )
            for collection in collections:
                logger.info(f"Dropping {collection}...")
                mdb.drop_collection(collection)

        logger.warning("Purge complete!")
