# pylint: disable = W0703, C0301, E0213, C0103, W0621, E0211,R1704, E1101,R0914, E1133,W0611
""" the MongoDB Database"""
import csv
import os
import pprint
import pathlib
import types
import time
from pymongo import MongoClient

TIMING_FILE = 'timings.txt'
open(TIMING_FILE, 'w').close()      #clean our timing file


class MongoDBConnection:
    """ Make the database connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def time_func(fn):
    """ this function is to wrap all our database function with timing"""
    def fn_composite(*args, **kwargs):
        start = time.perf_counter()
        rt = fn(*args, **kwargs)
        stop = time.perf_counter()
        fl = open(TIMING_FILE, 'a')
        report = f"{fn.__qualname__} took {stop - start} seconds to process {rt[1]} data\n"
        fl.write(report)
        print("Executing %s took %s seconds." % (fn.__qualname__, stop - start))
        return rt

    # return the composite function
    return fn_composite


class Timed(type):
    """ Meta class to add timing attribute for each function of our data base processor"""
    def __new__(cls, name, bases, attr):
        # replace each function with
        # a new function that is timed
        # run the computation with the provided args and return the computation result
        for name, value in attr.items():
            if callable(value):
                attr[name] = time_func(value)

        return super(Timed, cls).__new__(cls, name, bases, attr)


class HPNorton(metaclass=Timed):
    """ Database class for our warehouse"""

    def print_mdb_collection(collection_name):
        '''
        Prints the documents in columns.  May address this later, may not
        '''
        for doc in collection_name.find():
            pprint.pprint(doc)

    def import_data():
        """ import data from csv file to database"""
        directory_name = pathlib.Path(__file__).parent / "data"
        product_file = "product.csv"
        customer_file = "customer.csv"
        rental_file = "rental.csv"
        product_file_path = os.path.join(directory_name, product_file)
        customer_file_path = os.path.join(directory_name, customer_file)
        rental_file_path = os.path.join(directory_name, rental_file)
        client = MongoDBConnection()
        with client:
            # mongodb database;
            hp_norton_db = client.connection.hpnorton
            # collection in database
            product = hp_norton_db["product"]
            customer = hp_norton_db["customer"]
            rental = hp_norton_db["rental"]
            # delete all data in collection that we can check the code in several tests
            product.delete_many({})
            customer.delete_many({})
            rental.delete_many({})
            # write data in collections
            product_result = HPNorton.write_to_collection(product_file_path, product)
            customer_result = HPNorton.write_to_collection(customer_file_path, customer)
            rental_result = HPNorton.write_to_collection(rental_file_path, rental)
            return tuple(zip(product_result, customer_result, rental_result)), \
                   product_result[1] + customer_result[1] + rental_result[1]

    def write_to_collection(file_name, collection):
        """ write document into the collection"""
        try:
            file_handler = open(file_name, newline='')
            rows = csv.reader(file_handler)
            header = next(rows)
            # remove the weird prefix created for the first item in header
            if header[0].startswith("ï»¿"):
                header[0] = header[0][3:]
            row = csv.DictReader(file_handler, fieldnames=header)
            collection.insert_many(row)
            collection_count = collection.count_documents({})
            return 0, collection_count
        except Exception:
            return 0, 1
        finally:
            file_handler.close()

    def show_available_products():
        """ return the available product"""
        client = MongoDBConnection()
        with client:
            # mongodb database;
            hp_norton_db = client.connection.hpnorton
            query = {'qantity_available': {'$gt': '1'}}  # item with quantity more or equal to 1
            result = hp_norton_db.product.find(query, {'_id': 0})
            # make the return result as per assignment a dictionary of available products
            available_product = {}
            for doc in result:
                available_product.update({list(doc.values())[0]: dict(list(doc.items())[1:])})
            # pprint.pprint(available_product)
            return available_product, len(available_product)

    def show_rentals(product_id):
        """ return the customers that rent specific product"""
        client = MongoDBConnection()
        with client:
            # mongodb database;
            hp_norton_db = client.connection.hpnorton
            result = hp_norton_db.rental.find({'product_id': product_id})
            rental_users = {}
            for user in result:
                doc = hp_norton_db.customer.find_one({'Id': user['user_id']}, {'_id': 0})
                rental_users.update({list(doc.values())[0]: dict(list(doc.items())[1:])})
            return rental_users, len(rental_users)

    def drop_collection(collection):
        """ drop the collection"""
        client = MongoDBConnection()
        with client:
            # mongodb database;
            hp_norton_db = client.connection.hpnorton
            count = 0
            for collec in collection:
                count += 1
                hp_norton_db.drop_collection(collec)
        return count, count


print(HPNorton.import_data())
print(HPNorton.show_available_products())
print(HPNorton.show_rentals('P000001'))
collection = ['product', 'rental', 'customer']
HPNorton.drop_collection(collection)
