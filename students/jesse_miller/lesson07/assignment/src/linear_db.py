#!/usr/bin/env python3
# pylint: disable=C0103, W0621, W1203
'''
Mongo DB assignment for Python 220.  This one I get a bit better than the last
Actually, turns out that's a lie.  This is a giant rabbit hole.
'''
import csv
import logging
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
        logging.info(f'{filename} imported')
        return dict_list


def _add_bulk_data(collection, directory_name, filename):
    '''
    Adds data in bulk to database.
    '''
    file_path = os.path.join(directory_name, filename)

    initial_records = collection.count_documents({})

    collection.insert_many(_import_csv(file_path), ordered=False)

    final_records = collection.count_documents({})
    records_processed = final_records - initial_records

    return records_processed, initial_records, final_records #, run_time


def import_data(db, directory_name, products_file, customers_file, rentals_file):
    '''
    Function to import data into three MongoDB tables
    '''
    product_errors = 0
    customer_errors = 0
    rental_errors = 0
    directory_name = directory_name
    try:
        products = db['products']
        products.insert_many(_import_csv(products_file))
    except ImportError:
        product_errors += 1
    try:
        customers = db['customers']
        customers.insert_many(_import_csv(customers_file))
    except ImportError:
        customer_errors += 1
    try:
        rentals = db['rentals']
        rentals.insert_many(_import_csv(rentals_file))
    except ImportError:
        rental_errors += 1

    record_count = (db.products.count_documents({}),
                    db.customers.count_documents({}),
                    db.rentals.count_documents({}))

    error_count = (product_errors, customer_errors, rental_errors)
    logging.info('Database Populated')
    return record_count, error_count


def show_available_products(db):
    '''
    Returns a dictionary for each product that is available for rent
    (quantity > 0).
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

            customer_record = db.customers.find_one({'Id': customer_id})

            rental_users = {'name': customer_record['Name'] + ' ' +
                                    customer_record['Last_name'],
                            'address': customer_record['Home_address'],
                            'phone_number': customer_record['Phone_number'],
                            'email': customer_record['Email_address']}
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

        logging.info('\nShowing rental information for P000004')
        logging.info(show_rentals(db, 'P000004'))

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
