""" The main file for Jeremy Monroe Assignment 05 """

import logging
import csv
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


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Takes a dir name and three csv files. It populates a DATABAE with the data
    provdided and returns information about said data within two tuples.
    """
    parsed_product_file = parse_csv_input((directory_name + product_file))
    parsed_customer_file = parse_csv_input(directory_name + customer_file)
    parsed_rentals_file = parse_csv_input(directory_name + rentals_file)

    product_count = 0
    customer_count = 0
    rental_count = 0

    product_errors = 0
    customer_errors = 0
    rental_errors = 0

    try:
        with MONGO:
            DATABAE = MONGO.connection.assignment_05

            product_collection = DATABAE["product"]
            for product in parsed_product_file:
                product_collection.insert_one(product)

    except TypeError as excep:
        LOGGER.info("Error saving product info to database: %s", excep)
        product_errors = 1
    else:
        LOGGER.info("Successfully saved product info")
        product_count = len(parsed_product_file)

    try:
        with MONGO:
            DATABAE = MONGO.connection.assignment_05
            customer_collection = DATABAE["customer"]

            for customer in parsed_customer_file:
                customer_collection.insert_one(customer)
    except TypeError as excep:
        LOGGER.info("Error saving customer info to database: %s", excep)
        customer_errors = 1
    else:
        LOGGER.info("Successfully saved customer info.")
        customer_count = len(parsed_customer_file)

    try:
        with MONGO:
            DATABAE = MONGO.connection.assignment_05
            rental_collection = DATABAE["rental"]

            for rental in parsed_rentals_file:
                rental_collection.insert_one(rental)
    except TypeError as excep:
        LOGGER.info("Error saving rental info to database: %s", excep)
        rental_errors = 1
    else:
        LOGGER.info("Successfully saved rental info.")
        rental_count = len(parsed_rentals_file)

    return (
        (product_count, customer_count, rental_count),
        (product_errors, customer_errors, rental_errors),
    )


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
    Returns a dict containing information about products listed as available.
    """
    products_available = {}
    try:
        with MONGO:
            product_collection = MONGO.connection.assignment_05["product"].find()

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
    Returns a dict containing information about customers who have rented a
    product based on the provided product_id.
    """
    cust_rent_dict = {}
    try:
        with MONGO:
            DATABAE = MONGO.connection.assignment_05
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
        LOGGER.info("Error retrieving customer who rented product: %s", product_id)
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
    import_data("../data/", "product_with_error.csv", "customers.csv", "rental.csv")

    print(show_available_products())

    print(show_rentals("prd010"))

    TO_DROP_INPUT = input(
        "Do you want to drop the newly created database?" "\nY or N: "
    )
    if TO_DROP_INPUT.lower() == "y":
        with MONGO:
            TO_DROP = MONGO.connection
            TO_DROP.drop_database("assignment_05")
