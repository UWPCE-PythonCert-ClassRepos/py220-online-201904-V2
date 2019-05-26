"""
Jeremy Monroe Assignment_07

This is the original linear approach I took from assignment_05.
I did refactor import_data a bit because my code was not DRY at all.
"""

import logging
import csv
import argparse
from datetime import datetime
from pymongo import MongoClient

LOG_FORMAT = "\n%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s" "\n%(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MongoDatabaseConnection():
    """ MongoDATABAE Connection """

    def __init__(self, host="127.0.0.1", port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


MONGO = MongoDatabaseConnection()


def parse_cmd_arguments():# {{{
    """
    Parses the optional argument passed in at the command line to turn on
    logging to a file.

    Specifically so I can record timing improvements from various parts of my
    code.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-lf', '--logfile', nargs='?',
                        const=False, help='Log file on or off (true || false)')

    log_file_onoff = parser.parse_args()

    if log_file_onoff.logfile:
        formatter = logging.Formatter(("\n%(asctime)s"
                                       " %(filename)s:%(lineno)-3d"
                                       " %(levelname)s\n%(message)s"))

        log_file = "assignment_07" + '.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        LOGGER.addHandler(file_handler)# }}}


def import_data(directory_name, product_file, customer_file):
    """
    Takes a dir name and two csv files. It populates a database with the data
    provdided and returns information about said data within two tuples.
    """
    total_time_start = datetime.now()

    parsed_product_file = parse_csv_input((directory_name + product_file))
    parsed_customer_file = parse_csv_input(directory_name + customer_file)

    with MONGO:
        DATABAE = MONGO.connection.assignment_07

        product_count_prior = len(list(DATABAE.product.find()))
        customer_count_prior = len(list(DATABAE.customer.find()))

    start_product_insertion = datetime.now()

    save_parsed_data_to_db(parsed_product_file, 'product')

    end_product_insertion = datetime.now()
    LOGGER.info("Product insertion took: {}".format(end_product_insertion - start_product_insertion))

    save_parsed_data_to_db(parsed_customer_file, 'customer')

    end_customer_insertion = datetime.now()
    LOGGER.info("Customer insertion took: {}".format(end_customer_insertion - end_product_insertion))


    with MONGO:
        DATABAE = MONGO.connection.assignment_07

        product_count_new = len(list(DATABAE.product.find()))
        customer_count_new = len(list(DATABAE.customer.find()))

    total_time = str(datetime.now() - total_time_start)
    LOGGER.info("Total runtime = {}".format(total_time))
    return [(len(parsed_customer_file), customer_count_prior, customer_count_new, total_time), (len(parsed_product_file), product_count_prior, product_count_new, total_time)]




def save_parsed_data_to_db(parsed_file, collection_name):
    """
    Saves the data form parsed_file (a parsed csv file) to a mongodb database
    collection with the name specified by collection_name.
    """

    try:
        with MONGO:
            DATABAE = MONGO.connection.assignment_07

            new_collection = DATABAE[collection_name]
            for data_point in parsed_file:
                new_collection.insert_one(data_point)

    except TypeError as excep:
        LOGGER.info("Error saving product info to database: %s", excep)
        return False
    else:
        LOGGER.info("Successfully saved {} info".format(collection_name))
        return True


def parse_csv_input(input_file):
    """ Parses and returns an input csv file. """
    parsed_infile = []
    try:
        with open(input_file) as infile:
            for line in csv.reader(infile):
                parsed_infile.append(line)

        temp_object_storage = []

        for line_index, line in enumerate(parsed_infile[1:]):
            temp_object_storage.append({})
            for category_index, category in enumerate(parsed_infile[0]):
                if category_index == 0:
                    category = category[3:]
                temp_object_storage[line_index][category] = line[category_index]

        return temp_object_storage
    except FileNotFoundError as excep:
        LOGGER.info("error parsing csv file: %s", excep)


def show_available_products():
    """
    NOT USED FOR ASSIGNMENT 07

    Returns a dict containing information about products listed as available.
    """
    products_available = {}
    try:
        with MONGO:
            product_collection = MONGO.connection.assignment_07["product"].find(
            )

            for product in product_collection:
                if int(product["quantity_available"]) > 0:
                    products_available[product["product_id"]] = {
                        "description": product["description"],
                        "product_type": product["product_type"],
                        "quantity_available": product["quantity_available"],
                    }
    except TypeError as excep:
        LOGGER.warning("Error looking up available products")
        LOGGER.warning(excep)
    else:
        if not products_available:
            LOGGER.info('No products found')
        else:
            LOGGER.info("Available products retrieved successfully.")
            return products_available


def show_rentals(product_id):
    """
    NOT USED FOR ASSIGNMENT 07

    Returns a dict containing information about customers who have rented a
    product based on the provided product_id.
    """
    cust_rent_dict = {}
    try:
        with MONGO:
            DATABAE = MONGO.connection.assignment_07
            customer_rental = DATABAE.rental.aggregate(
                [
                    {
                        "$lookup": {
                            "from": "customer",
                            "localField": "user_id",
                            "foreignField": "user_id",
                            "as": "customer_rentals",
                        }
                    },
                    {"$match": {"product_id": product_id}},
                ]
            )
    except TypeError as excep:
        LOGGER.info(
            "Error retrieving customer who rented product: %s", product_id)
        LOGGER.info(excep)

    try:
        for customer in customer_rental:
            cust_rent_dict[customer["user_id"]] = {
                "name": customer["customer_rentals"][0]["name"],
                "address": customer["customer_rentals"][0]["address"],
                "phone_number": customer["customer_rentals"][0]["phone_number"],
                "email": customer["customer_rentals"][0]["email"],
            }
    except TypeError as excep:
        LOGGER.info("Error formatting retrieved customer rental info")
        LOGGER.info(excep)
    else:
        if not cust_rent_dict:
            LOGGER.info("Product: %s not found.", product_id)
        else:
            LOGGER.info('Retrieved rental info for product: %s', product_id)
            return cust_rent_dict


if __name__ == "__main__":
    parse_cmd_arguments()

    LOGGER.info(import_data("./data/", "test_product_100.csv",
                "test_customer_100.csv"))

    # LOGGER.info(import_data("./data/", "test_product_1000.csv",
    #             "test_customer_1000.csv"))

    # LOGGER.info(import_data("./data/", "product.csv",
    #            "customer.csv"))


    # print(show_available_products())

    # print(show_rentals("prd010"))

    TO_DROP_INPUT = input(
        "Do you want to drop the newly created database?" "\nY or N: "
    )
    if TO_DROP_INPUT.lower() == "y":
        with MONGO:
            TO_DROP = MONGO.connection
            TO_DROP.drop_database("assignment_07")
