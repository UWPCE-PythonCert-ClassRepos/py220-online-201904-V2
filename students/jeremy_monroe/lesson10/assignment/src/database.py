"""
Jeremy Monroe assignment 05 revisited for assignment 10

I've used a class decorator to implement timing and logging of all functions.
A second logger is implemented as a class variable in TimerDec and the __call__
method is used to call the function passed in with a datetime.now() start and
end variable on either side of the call.

The captured timing data is logged to timings.txt.

I've commented out the @TimerDec decorators because otherwise the log starts to
get really long when running tests and whatnot on database.py!
"""

import logging
import csv
from datetime import datetime
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MongoDatabaseConnection():  # {{{
    """ MongoDATABAE Connection """

    def __init__(self, host="127.0.0.1", port=27017):
        self.host = host
        self.port = port
        self.connection = None
        self.product_collection = None
        self.customer_collection = None
        self.rental_collection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.product_collection = self.connection.assignment_10['product']
        self.customer_collection = self.connection.assignment_10['customer']
        self.rental_collection = self.connection.assignment_10['rental']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()  # }}}


MONGO = MongoDatabaseConnection()


class TimerDec:
    """
    A class to be used as a decorator which will run the decorated function
    normally; and in addition will save the time it took to run the function to
    a log file.
    """

    LOG_FORMAT = ("\n%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s"
                  "\n%(message)s")
    FORMATTER = logging.Formatter(LOG_FORMAT)
    timer_log = logging.getLogger("timing_logger")
    timer_file_handler = logging.FileHandler('timings.txt')
    timer_file_handler.setFormatter(FORMATTER)
    timer_log.addHandler(timer_file_handler)

    def __init__(self, func_to_decorate):
        self.func_to_decorate = func_to_decorate

    def __call__(self, *args):
        start = datetime.now()
        func_return = self.func_to_decorate(*args)
        end = datetime.now()

        self.timer_log.info((f"Function {self.func_to_decorate.__name__}\n"
                             f"With args {args}\n"
                             f"Took {end - start} to run\n"))

        if self.func_to_decorate.__name__ == 'import_data':
            self.timer_log.info((f"\nNumber of records processed:\n"
                f"products = {func_return[0][0]} | customers = {func_return[0][1]}"
                f" | rentals = {func_return[0][2]}"
                ))
        return func_return


# @TimerDec
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Takes a dir name and three csv files. It populates a database with the data
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
            for product in parsed_product_file:
                try:
                    MONGO.product_collection.insert_one(product)
                except TypeError as excep:
                    LOGGER.info(
                        "Error saving product info to database: %s", excep)
                    product_errors += 1
                else:
                    product_count += 1

    except TypeError as excep:
        LOGGER.warning("Critical error, no products saved to database")
    else:
        LOGGER.info("Successfully saved product info")
        product_count = len(parsed_product_file)

    try:
        with MONGO:
            for customer in parsed_customer_file:
                try:
                    MONGO.customer_collection.insert_one(customer)
                except TypeError as excep:
                    LOGGER.info(
                        "Error saving customer info to database: %s", excep)
                    customer_errors += 1
                else:
                    customer_count += 1
    except TypeError as excep:
        LOGGER.warning("Critical error, no customers saved to database!")
    else:
        LOGGER.info("Successfully saved customer info.")
        customer_count = len(parsed_customer_file)

    try:
        with MONGO:
            for rental in parsed_rentals_file:
                try:
                    MONGO.rental_collection.insert_one(rental)
                except TypeError as excep:
                    LOGGER.info(
                        "Error saving rental info to database: %s", excep)
                    rental_errors += 1
                else:
                    rental_count += 1
    except TypeError as excep:
        LOGGER.info("Critical error, no rentals saved to database!")
    else:
        LOGGER.info("Successfully saved rental info.")
        rental_count = len(parsed_rentals_file)

    return (
        (product_count, customer_count, rental_count),
        (product_errors, customer_errors, rental_errors),
    )


# @TimerDec
def parse_csv_input(input_file):  # {{{
    """
    Parses and returns an input csv file as a list of lists.
    """
    parsed_infile = []
    try:
        with open(input_file) as infile:
            # Starts by opening the specified file
            for line in csv.reader(infile):
                # Saves each line of opened file to a list.
                parsed_infile.append(line)

        temp_object_storage = []

        for line_index, line in enumerate(parsed_infile[1:]):
            # a dict is appended to an empty list for each line in the newly
            # parsed csv file.
            temp_object_storage.append({})
            for category_index, category in enumerate(parsed_infile[0]):
                # Then, loop over each item in each line and append it to the
                # newly appended empty dicts using the categories defined on the
                # first line of the csv file as the keys.

                # this if statement is just to remove unnecessary characters at
                # the start of one of the categories.
                if category_index == 0:
                    category = category

                temp_object_storage[line_index][category] = line[category_index]

        return temp_object_storage
    except FileNotFoundError as excep:
        LOGGER.info("error parsing csv file: %s", excep)  # }}}


# @TimerDec
def show_available_products():  # {{{
    """
    Returns a dict containing information about products listed as available.
    """
    products_available = {}
    try:
        with MONGO:
            product_collection = (MONGO.product_collection.find())

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
            return {}
        LOGGER.info("Available products retrieved successfully.")
        return products_available  # }}}


# @TimerDec
def show_rentals(product_id):  # {{{
    """
    Returns a dict containing information about customers who have rented a
    product based on the provided product_id.
    """
    cust_rent_dict = {}
    try:
        with MONGO:
            # DATABAE = MONGO.connection.assignment_05
            customer_rental = MONGO.rental_collection.aggregate(
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
        LOGGER.info(("Error retrieving customer who"
                     "rented product: %s"), product_id)
        LOGGER.info(excep)

    try:
        for customer in customer_rental:
            cust_rent_dict[customer["user_id"]] = {
                "name": customer["name"],
                "address": customer["address"],
                "phone_number": customer['phone_number'],
                'email': customer['email']
            }
    except TypeError as excep:
        LOGGER.info("Error formatting retrieved customer rental info")
        LOGGER.info(excep)
    else:
        if not cust_rent_dict:
            LOGGER.info("Product: %s not found.", product_id)
            return {}
        LOGGER.info('Retrieved rental info for product: %s', product_id)
        return cust_rent_dict  # }}}


if __name__ == "__main__":
    # import_data("../data/", "product.csv",
    #             "customer.csv", "rental.csv")
    import_data("../data/", "test_product.csv",
                "test_customer.csv", "test_rental.csv")

    # print(f'Len show_available_products = { len(show_available_products()) }')

    show_available_products()
    show_rentals("P000259")

    # print(parse_csv_input('../data/test_rental.csv'))

    TO_DROP_INPUT = input(
        "Do you want to drop the newly created database?" "\nY or N: "
    )
    if TO_DROP_INPUT.lower() == "y":
        with MONGO:
            TO_DROP = MONGO.connection
            TO_DROP.drop_database("assignment_10")
