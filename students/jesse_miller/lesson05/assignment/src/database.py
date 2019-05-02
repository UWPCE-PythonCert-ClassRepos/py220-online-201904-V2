#!/usr/bin/env python3
'''
Mongo DB assignment for Python 220.  This one I get a bit better than the last
Actually, turns out that's a lie.  This is a giant rabbit hole.
'''
import csv
import os
import logging
import logging_config
import pymongo

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


def print_mdb_collection(collection_name):
    '''
    Prints the documents in columns.  May address this later, may not
    '''
    for doc in collection_name.find():
        print(doc)


def _import_csv(filename):
    '''
    This returns a list of the stored dictionaries.  One per row.
    filename = .csv file
    return = list of dictionaries
    '''
    with open(filename, newline='') as csvfile:
        dict_list = []

        csv_data = csv.reader(csvfile)

        headers = next(csv_data, None)

    if headers[0].startswith('ï»¿'):  # Check for weird formatting
        headers[0] = headers[0][3:]

    for row in csv_data:
        row_dict = {}

        for index, column in enumerate(headers):
            row_dict[column] = row[index]

        dict_list.append(row_dict)
    return dict_list


def _add_bulk_data(collection, directory_name, filename):
    '''
    This, if it works properly, will handle the bulk imports from the csv
    files.
    '''
    file_path = os.path.join(directory_name, filename)

    try:
        collection.insert_many(_import_csv(file_path), ordered=False)
        return 0

    except pymongo.errors.BulkWriteError as bwe:
        print(bwe.details)
        return len(bwe.details['writeErrors'])


def import_data(d_base, directory_name, products_file, customers_file,
                rentals_file):
    '''
    This takes the three files and the src directory, and loads said files in
    the database.
     db: self explanatory
     directory_name: directory name for files
     products_file: csv file for product data
     customers_file: csv file for customer data
     rentals_file: csv file for rentals data
    '''

    products = d_base['products']
    products_errors = _add_bulk_data(products, directory_name, products_file)

    customers = d_base['customers']
    customers_errors = _add_bulk_data(customers, directory_name, customers_file)

    rentals = d_base['rentals']
    rentals_errors = _add_bulk_data(rentals, directory_name, rentals_file)

    record_count = (d_base.products.count_documents({}), \
                    d_base.customers.count_documents({}), \
                    d_base.rentals.count_documents({}))

    error_count = (products_errors, customers_errors, rentals_errors)

    return record_count, error_count


def show_available_products(d_base):
    '''
    Returns a dictionary showing available product.
    '''

    available_products = {}

    for product in d_base.products.find():
        if int(product['quantity_available']) > 0:
            products_list = {'description': product['description'],
                             'product_type': product['product_type'],
                             'quantity_available': product['quantity_available']}

            available_products[product['product_id']] = products_list

    return available_products


def show_rentals(d_base, product_id):
    '''
    Returns a dictionary with renter information from users who have products
    that match the product_id.
    '''

    customer_info = {}

    for rental in d_base.rentals.find():
        if rental['product_id'] == product_id:
            customer_id = rental['user_id']

            customer_record = d_base.customers.find_one({'user_id': customer_id})

            customer_dict = {'name': customer_record['name'],
                             'address': customer_record['address'],
                             'phone_number': customer_record['phone_number'],
                             'email': customer_record['email']}

            customer_info[customer_id] = customer_dict

    return customer_info


def clear_data(d_base):
    '''
    Delete data in the database.
    '''
    d_base.products.drop()
    d_base.customers.drop()
    d_base.rentals.drop()
