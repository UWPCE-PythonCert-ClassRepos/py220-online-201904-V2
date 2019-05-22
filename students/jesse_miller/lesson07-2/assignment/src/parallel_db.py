'''
Lesson 07:  Linear DB loading
'''
# pylint: disable=C0103
import csv
import os
import logging
import time
from pathlib import Path
from timeit import timeit
import threading
from line_profiler import LineProfiler
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
        self.connection = pymongo.MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    '''
    Prints all documents in a collection.
    '''
    for doc in collection_name.find():
        print(doc)


def import_data(filename):
    '''
    Returns a list of dictionaries.  One dictionary for each row of data in a
    csv file.
    '''
    filename = Path.cwd().with_name('data') / filename
    with open(filename, newline='') as csvfile:
        dict_list = []

        csv_data = csv.reader(csvfile)

        headers = next(csv_data, None)

        if headers[0].startswith('ï»¿'):
            headers[0] = headers[0][3:]

        for row in csv_data:
            row_dict = {column: row[index] for index, column in \
            enumerate(headers)}

            dict_list.append(row_dict)

        return dict_list


def _add_bulk_data(results, collection, directory_name, filename):
    '''
    Adds data in bulk to database.
    '''
    file_path = os.path.join(directory_name, filename)

    start_time = time.time()
    initial_records = collection.count_documents({})

    collection.insert_many(_import_csv(file_path), ordered=False)

    final_records = collection.count_documents({})
    records_processed = final_records - initial_records
    run_time = time.time() - start_time

    stats = (records_processed, initial_records, final_records, run_time)

    results[collection.name] = stats


def import_data(db, directory_name, products_file, customers_file, rentals_file):
    '''
    Takes a directory name and three csv files as input.  Creates and populates
    three collections in MongoDB.
    '''

    products = db['products']
    customers = db['customers']
    rentals = db['rentals']

    results_dict = {}

    threads = [threading.Thread(target=_add_bulk_data, args=(results_dict,
                                                             products,
                                                             directory_name,
                                                             products_file)),
               threading.Thread(target=_add_bulk_data, args=(results_dict,
                                                             customers,
                                                             directory_name,
                                                             customers_file)),
               threading.Thread(target=_add_bulk_data, args=(results_dict,
                                                             rentals,
                                                             directory_name,
                                                             rentals_file))]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return [results_dict['customers'], results_dict['products']]


def show_available_products(db):
    '''
    Returns a dictionary for each product listed as available.
    '''

    available_products = {}

    for product in db.products.find():
        if product['quantity_available'] != '0':
            rental_users = {key: value for key, value in product.items() if \
                          key not in ('_id', 'product_id')}
            available_products[product['product_id']] = rental_users

    return available_products


def show_rentals(db, product_id):
    '''
    Returns a dictionary with user information from users who have rented
    products matching the product_id.
    '''

    customer_info = {}

    for rental in db.rentals.find():
        if rental["product_id"] == product_id:
            customer_id = rental["user_id"]
            customer_record = db.customers.find_one({"user_id": customer_id})

            short_dict = {key: value for key, value in customer_record.items() \
            if key not in ("_id", "user_id")}
            customer_info[customer_id] = short_dict

        return customer_info


def clear_data(db):
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

        logging.info('\nShowing rental information for prd005')
        logging.info(show_rentals(db, 'prd005'))

        logging.info('\nClearing data from database.')
        clear_data(db)

    return results


if __name__ == '__main__':
    main()
    print(timeit('main()', globals=globals(), number=1))
    print(timeit('main()', globals=globals(), number=10))

    lp = LineProfiler()
    lp_wrapper = lp(main)
    lp_wrapper()
    lp.print_stats()
