""""
Lesson 5. Create DB using mongodb api
"""

# pylint: disable= W1203, R0914, C0103, W0703, W0612, R0201
import logging
import csv
import os
import time
from pymongo import MongoClient  # high level api


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)


class MongoDBConnection():
    """
    Class to start MongoDB Connection
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def get_time(func):
    '''
    method to get time for each function
    '''
    def calc_time(*args, **kwargs):
        start = time.time()
        results = func(*args, **kwargs)
        total_time = time.time() - start
        with open("timings.txt", "a+") as file:
            file.write(f'{func.__name__} took {total_time} seconds to run\n')
        return results
    return calc_time


class Timed(type):
    """ Meta class to add timing """
    def __new__(cls, clsname, bases, clsdict):
        for name, value in clsdict.items():
            if callable(value):
                clsdict[name] = get_time(value)

        return super(Timed, cls).__new__(cls, clsname, bases, clsdict)


class database(metaclass=Timed):
    '''
    class to make database and add data to it
    '''
    def import_data(
            self,
            directory_name,
            product_file,
            customer_file,
            rentals_file):
        """
        method to import the csv files that will be added to the db
        """
        LOGGER.info("starting MongoDBConnection")
        mongo = MongoDBConnection()

        with mongo:

            # mongodb database; it all starts here
            db = mongo.connection.HPNorton

            # collection in database
            products = db["products"]
            customers = db["customers"]
            rentals = db["rentals"]
            db.products.drop()
            db.customers.drop()
            db.rentals.drop()

            LOGGER.info("importing data")
            product_ip = database.read_data(self, directory_name, product_file)
            customer_ip = database.read_data(
                self, directory_name, customer_file)
            rentals_ip = database.read_data(self, directory_name, rentals_file)

            product_results = database.add_many_ip(self, products, product_ip)
            customer_results = database.add_many_ip(
                self, customers, customer_ip)
            rental_results = database.add_many_ip(self, rentals, rentals_ip)

        import_count = (
            db.products.count_documents({}),
            db.customers.count_documents({}),
            db.rentals.count_documents({})
        )

        LOGGER.info(f'succesful product imports = {import_count[0]} to db')
        LOGGER.info(f'succesful customer imports = {import_count[1]} to db')
        LOGGER.info(f'succesful rental imports = {import_count[2]} to db')

        error_count = (product_results, customer_results, rental_results)
        LOGGER.info(f'product import errors = {error_count[0]} to db')
        LOGGER.info(f'customer import errors = {error_count[1]} to db')
        LOGGER.info(f'rental import errors = {error_count[2]} to db')

        return import_count, error_count

    def read_data(self, directory_name, file_name):
        """
        method to read in the csv files
        """
        LOGGER.info(f'reading {file_name} data from {directory_name}')
        ip_list = []

        try:
            with open(directory_name + file_name) as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader, None)
                header[0] = header[0].replace("\ufeff", "")

                for row in reader:
                    temp_dict = {}
                    for index, value in enumerate(header):
                        temp_dict[value] = row[index]
                    ip_list.append(temp_dict)
            LOGGER.info("successfully read in data")

        except Exception as error:
            LOGGER.info(f'could not read data due to {error}')

        return ip_list

    def add_many_ip(self, collection_name, collection_ip):
        """
        method to add the data to the collection
        """

        try:
            collection_name.insert_many(collection_ip)
            LOGGER.info(f'no errors importing to {collection_name} ')
            error = 0
            return error
        except Exception as error:
            LOGGER.info(
                f'add_many_ip error of {error} for to {collection_name}')
            error = 1
            return error

    def show_available_products(self):
        """
        Method to show available products
        """
        mongo = MongoDBConnection()
        LOGGER.info("starting show_available_products method")
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.HPNorton
            avail_products_dict = {}
            query = {'quantity_available': {'$gt': '1'}}
            for query_results in db.products.find(query):
                key = query_results["product_id"]
                values = {
                    "description": query_results["description"],
                    "product_type": query_results["product_type"],
                    "quantity_available": query_results["quantity_available"]
                }
                temp_dict = {key: values}
                avail_products_dict.update(temp_dict)
        LOGGER.info(f'available products = {avail_products_dict}')
        return avail_products_dict

    def show_rentals(self, product_id):
        """
        Method to show available products
        """
        mongo = MongoDBConnection()
        LOGGER.info("starting show_rentals method")
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.HPNorton
            show_rentals_dict = {}
            query = {'product_id': product_id}
            for query_results in db.rentals.find(query):
                query_2 = {'user_id': query_results['user_id']}
                for query_results_2 in db.customers.find(query_2):
                    key = query_results_2['user_id']
                    value = {
                        'name': query_results_2['name'],
                        'address': query_results_2['address'],
                        'phone_number': query_results_2['phone_number'],
                        'email': query_results_2['email']
                    }
                    temp_dict = {key: value}
                    show_rentals_dict.update(temp_dict)
        LOGGER.info(
            f'showing rentals that match "{product_id}" = {show_rentals_dict}')

        return show_rentals_dict

    def drop_data(self):
        """
        method to drop the data from db
        """
        mongo = MongoDBConnection()
        LOGGER.info("starting drop data method")
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.HPNorton
            db.products.drop()
            db.customers.drop()
            db.rentals.drop()


def main():
    """
    main used to call other methods
    """
    cwd = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    db = database()
    import_count, error_count = db.import_data(
        cwd + "/", "product.csv", "customers.csv", "rental.csv")
    db.show_available_products()
    db.show_rentals("prd002")
    db.drop_data()
    db2 = database()
    import_count, error_count = db2.import_data(
        cwd + "/", "product.1.csv", "customers.1.csv", "rental.1.csv")
    db2.show_available_products()
    db2.show_rentals("prd002")
    db2.drop_data()
    db3 = database()
    import_count, error_count = db3.import_data(
        cwd + "/", "product.2.csv", "customers.2.csv", "rental.2.csv")
    db3.show_available_products()
    db3.show_rentals("prd002")
    db3.drop_data()


if __name__ == "__main__":
    main()
