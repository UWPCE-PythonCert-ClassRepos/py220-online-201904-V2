#!/usr/bin/env python3
# pylint: disable=C0103, W0621, W1203
'''
Mongo DB assignment for Python 220.  This one I get a bit better than the last
Actually, turns out that's a lie.  This is a giant rabbit hole.
'''
import csv
import logging
# import time
import os
from timeit import timeit
from pathlib import Path
import pymongo
from line_profiler import LineProfiler


logging.basicConfig(filename='example.log', level=logging.DEBUG)


class MongoDBConnection:
    '''
    Creating the connection to the Mongo daemon
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
    logging.info('Database connected')


def print_mdb_collection(collection_name):
    '''
    Prints all documents in a collection.
    '''
    for doc in collection_name.find():
        print(doc)


def _import_csv(filename):
    '''
    This function imports the .csv files containing our data.
    '''
    filename = Path.cwd().with_name('data') / filename
    with open(filename, newline='', encoding='utf-8') as file:
        dict_list = []
        csv_data = csv.reader(file)
        headers = next(csv_data, None)
        if headers[0].startswith('\ufeff'):
            headers[0] = headers[0][1:]

        for row in csv_data:
            row_dict = {}
            for index, column in enumerate(headers):
                row_dict[column] = row[index]

            dict_list.append(row_dict)
        logging.info(f'{filename}.csv imported')
        return dict_list


def _add_bulk_data(collection, directory_name, filename):
    '''
    Adds data in bulk to database.
    '''
    file_path = os.path.join(directory_name, filename)

    # start_time = time.time()
    initial_records = collection.count_documents({})

    collection.insert_many(_import_csv(file_path), ordered=False)

    final_records = collection.count_documents({})
    records_processed = final_records - initial_records
    # run_time = time.time() - start_time

    return records_processed, initial_records, final_records #, run_time


def import_data(db, directory_name, products_file, customers_file, rentals_file):
    '''
    Function to import data into three MongoDB tables
    '''
    products = db['products']
    products_results = _add_bulk_data(products, directory_name, products_file)

    customers = db['customers']
    customers_results = _add_bulk_data(customers, directory_name, customers_file)

    rentals = db['rentals']
    rentals_results = _add_bulk_data(rentals, directory_name, rentals_file)

    return [products_results, customers_results, rentals_results]


def show_available_products(db):
    '''
    Returns a dictionary for each product that is available for rent (quantity > 0).
    '''
    available_products = {}
    for product_id in db.products.find():
        product_dict = {'description': product_id['description'],
                        'product_type': product_id['product_type'],
                        'quantity_available': product_id['quantity_available']}
        if product_id['quantity_available'] != '0':
            available_products[product_id['product_id']] = product_dict

    return available_products


def show_rentals(db, product_id):
    '''
    Function to look up customers who have rented a specific product.
    '''
    rental_users_dict = {}

    for rental in db.rentals.find():
        if rental['product_id'] == product_id:
            customer_id = rental['user_id']
            print(customer_id)

            customer_record = db.customers.find_one({'user_id': customer_id})
            print(customer_record)

            rental_users = {'name': customer_record['name'],
                            'address': customer_record['address'],
                            'phone_number': customer_record['phone_number'],
                            'email': customer_record['email']}

            rental_users_dict[customer_id] = rental_users
        return rental_users_dict


def clear_data(db):
    '''
    Clear database
    '''
    db.products.drop()
    db.customers.drop()
    db.rentals.drop()


def main():
    '''
    Main execution
    '''
    mongo = MongoDBConnection()

    with mongo:
        logging.info('Opening MongoDB')
        db = mongo.connection.media

        logging.info('Importing csv files')
        import_data(db, '', 'product.csv', 'customer.csv', 'rental.csv')

        logging.info('Showing available products')
        logging.info(show_available_products(db))

        logging.info('\nShowing rental information for P000003')
        logging.info(show_rentals(db, 'P000003'))
        print(show_rentals(db, 'P000004'))

        logging.info('\nClearing data from database.')
        clear_data(db)


if __name__ == '__main__':
    main()

    print(timeit('main()', globals=globals(), number=1))
    print(timeit('main()', globals=globals(), number=10))

    lp = LineProfiler()
    lp_wrapper = lp(main)
    lp_wrapper()
    lp.print_stats()
