""""
Lesson 5. Create DB using mongodb api
"""

from pymongo import MongoClient #high level api
import glob
import logging
import csv

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(formatter)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)


class MongoDBConnection(object):
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

def import_data(directory_name, product_file, customer_file, rentals_file):
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

        LOGGER.info("importing data")
        product_ip = read_data(directory_name,product_file)
        customer_ip = read_data(directory_name,customer_file)
        rentals_ip = read_data(directory_name,rentals_file)

        product_results = add_many_ip(products, product_ip)
        customer_results = add_many_ip(customers, customer_ip)
        rental_results = add_many_ip(rentals, rentals_ip)


    import_count = (product_results[0], customer_results[0], rental_results[0])
    LOGGER.info(f'succesful product imports = {import_count[0]} to db')
    LOGGER.info(f'succesful customer imports = {import_count[1]} to db')
    LOGGER.info(f'succesful rental imports = {import_count[2]} to db')

    error_count = (product_results[1], customer_results[1], rental_results[1])
    LOGGER.info(f'product import errors = {error_count[0]} to db')
    LOGGER.info(f'customer import errors = {error_count[1]} to db')
    LOGGER.info(f'rental import errors = {error_count[2]} to db')

    return import_count, error_count








def read_data(directory_name,file_name):
    """
    method to read in the csv files
    """
    LOGGER.info(f'reading {file_name} data from {directory_name}')
    ip_list = []

    try:
        with open(directory_name+file_name) as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader, None)
            header[0]=header[0].replace("\ufeff","")

            for row in reader:
                temp_dict={}
                for index, value in enumerate(header):
                    temp_dict[value] = row[index]
                ip_list.append(temp_dict)
        LOGGER.info("successfully read in data")

    except Exception as error:
        LOGGER.info(f'could not read data due to {error}')

    return ip_list

def add_many_ip(collection_name,collection_ip):
    """
    method to add the data to the collection
    """

    try:
        collection_name.insert_many(collection_ip)
        LOGGER.info(f'no errors importing to {collection_name} ')
        insert = 1
        error = 0
        return [insert,error]
    except Exception as error:
        LOGGER.info(f'add_many_ip error of {error} for to {collection_name}')
        insert = 0
        error = 1
        return [insert,error]


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)

def show_available_products():
    """
    Method to show available products
    """
    mongo = MongoDBConnection()
    LOGGER.info("starting show_available_products method")
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.HPNorton
        query = {'quantity_available': {'$gt': '1'}}
        avail_products_dict = {}
        for query_results in db.products.find(query):
            key = query_results["product_id"]
            values = {
                "description" : query_results["description"],
                "product_type" : query_results["product_type"],
                "quantity_available" : query_results["quantity_available"]
                }
            temp_dict = {key:values}
            avail_products_dict.update(temp_dict)
        print(avail_products_dict)

def drop_data():
    mongo = MongoDBConnection()
    LOGGER.info("starting drop data method")
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.HPNorton
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()




def main():

    import_count, error_count = import_data("../data/", "product.csv", "customers.csv", "rental.csv")
    show_available_products()
    drop_data()

if __name__== "__main__":
    main()

