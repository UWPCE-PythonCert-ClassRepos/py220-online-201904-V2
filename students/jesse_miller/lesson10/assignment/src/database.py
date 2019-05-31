'''
Lesson 10:  Metaprogramming
First thing I did was remove the timeit and lineprofiler calls.  We're obviously
replacing them with a timing function.
'''
# pylint: disable=C0103,R1710,R0913,R0903,R0201
import csv
import os
import logging
import time
from pathlib import Path
import threading
import types
import pymongo


class MongoDBConnection:
    '''
    Creates a MongoDB Connection
    '''
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        print('Opening a MongoDB connection.\n')
        self.connection = pymongo.MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('\nClosing the MongoDB connection.')
        self.connection.close()


def print_mdb_collection(collection_name):
    '''
    Prints all documents in a collection.
    '''
    for doc in collection_name.find():
        print(doc)


def timing_wrapper(func):
    '''
    This will return a new function that encapsulates the timing of the
    execution of function passed in the function.  Man that's confusing.
    Just, lookit, below here are timing functions that the executable
    functions in this program will pass through.
    '''
    def timing_function(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        time_elapsed = time.time() - start

        mongo = MongoDBConnection()

        with mongo:
            db = mongo.connection.media

            record_count = (db.products.count_documents({}),
                            db.customers.count_documents({}),
                            db.rentals.count_documents({}))

            time_results = f"{func.__name__}, {time_elapsed}, {record_count}\n"

        with open("timings.csv", "a+") as file:
            file.write(time_results)

        return result
    return timing_function


class MetaTimer(type):
    '''
    Metaclass that replaces class methods with timed methods.
    '''

    def __new__(cls, name, bases, attr):
        '''
        Replace each function with a new function that is timed.
        Returns result from original function.
        '''
        for key, value in attr.items():
            if isinstance(value, (types.FunctionType, types.MethodType)):
                attr[key] = timing_wrapper(value)

        return super(MetaTimer, cls).__new__(cls, name, bases, attr)


class Database(metaclass=MetaTimer):
    '''
    Class to encap the original database program
    '''

    def _import_csv(self, filename):
        '''
        Returns a list of dictionaries.  One dictionary for each row of data in
        a csv file.
        '''
        filename = Path.cwd().with_name('data') / filename
        with open(filename, newline='') as csvfile:
            dict_list = []
            csv_data = csv.reader(csvfile)
            headers = next(csv_data, None)  # Save the first line as the headers

            if headers[0].startswith('ï»¿'):  # Check for weird formatting
                headers[0] = headers[0][3:]

            for row in csv_data:
                row_dict = {column: row[index] for index, column in \
                enumerate(headers)}

                dict_list.append(row_dict)

            return dict_list


    def _add_bulk_data(self, collection, directory_name, filename):
        '''
        Adds data in bulk to database.
        '''
        file_path = os.path.join(directory_name, filename)

        try:
            collection.insert_many(Database._import_csv(self, file_path),
                                   ordered=False)
            return 0

        except pymongo.errors.BulkWriteError as bwe:
            print(bwe.details)
            return len(bwe.details["writeErrors"])


    def import_data(self, db, directory_name, products_file, customers_file,
                    rentals_file):
        '''
        Takes a directory name and three csv files as input.  Creates and
        populates three collections in MongoDB.
        '''

        products = db['products']
        customers = db['customers']
        rentals = db['rentals']

        results_dict = {}

        threads = [threading.Thread(
            target=self._add_bulk_data, args=(results_dict,
                                              products,
                                              directory_name,
                                              products_file)),
                   threading.Thread(
                       target=self._add_bulk_data, args=(results_dict,
                                                         customers,
                                                         directory_name,
                                                         customers_file)),
                   threading.Thread(
                       target=self._add_bulk_data, args=(results_dict,
                                                         rentals,
                                                         directory_name,
                                                         rentals_file))]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        return [results_dict['customers'], results_dict['products'],
                results_dict['rentals']]


    def show_available_products(self, db):
        '''
        Returns a dictionary for each product listed as available.
        '''

        available_products = {}

        for product in db.products.find():
            if product['quantity_available'] != '0':
                rental_users = {key: value for key, value in product.items() \
                    if key not in ('_id', 'product_id')}
                available_products[product['product_id']] = rental_users

        return available_products


    def show_rentals(self, db, product_id):
        '''
        Function to look up customers who have rented a specific product.
        '''
        rental_users_dict = {}

        for rental in db.rentals.find():
            if rental['product_id'] == product_id:
                customer_id = rental['user_id']

                customer_record = db.customers.find_one({'Id': customer_id})

                rental_users = {'name': customer_record['Name'] + ' ' +
                                        customer_record['Last_name'],
                                'address': customer_record['Home_address'],
                                'phone_number': customer_record['Phone_number'],
                                'email': customer_record['Email_address']}
                rental_users_dict[customer_id] = rental_users

        return rental_users_dict


    def clear_data(self, db):
        '''
        Delete data in MongoDB.
        '''
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()


def main():
    '''
    Main function
    '''
    mongo = MongoDBConnection()

    with mongo:
        logging.info('Opening MongoDB')
        db = mongo.connection.media

        logging.info('Importing csv files')
        results = import_data(db, '', 'product.csv', 'customer.csv',
                              'rental.csv')

        logging.info('Showing available products')
        logging.info(show_available_products(db))

        logging.info('\nShowing rental information for P000004')
        logging.info(show_rentals(db, 'P000004'))

        logging.info('\nClearing data from database.')
        clear_data(db)

    return results


if __name__ == '__main__':
    main()
