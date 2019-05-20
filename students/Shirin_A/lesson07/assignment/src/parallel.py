"""
Concurrency & Async Programming
"""
# pylint: disable= C0303

import csv
import os
import time
from timeit import timeit 
import threading
import pymongo



class MongoDBConnection:

    """
    Creates a MongoDB Connection
    """

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
    """
    Prints all documents in a collection.
    :param collection_name: collection
    """
    for doc in collection_name.find():
        print(doc)

def import_csv(filename):
    """
    Returns a list of dictionaries.  One dictionary
    for each row of data in a csv file.

    :return: list of dictionaries

    """
    with open(filename, newline="") as csvfile:
        dict_list = []
        csv_data = csv.reader(csvfile)
        headers = next(csv_data, None)  
        if headers[0].startswith("ï»¿"):  # Check for weird formatting

            headers[0] = headers[0][3:]
        for row in csv_data:
            row_dict = {column: row[index] for index, column in enumerate(headers)}
            dict_list.append(row_dict)
        return dict_list

def add_bulk_data(results, collection, directory_name, filename):

    """
    Adds data in bulk to database.
    :param collection: collection
    :param directory_name: directory
    :param filename: csv file
    :return: records processed (int), initial records (int),
     final records (int), function run time (float)
    """

    file_path = os.path.join(directory_name, filename)
    start_time = time.time()
    initial_records = collection.count_documents({})
    collection.insert_many(import_csv(file_path), ordered=False)

    final_records = collection.count_documents({})

    records_processed = final_records - initial_records
    run_time = time.time() - start_time
    stats = (records_processed, initial_records, final_records, run_time)
    results[collection.name] = stats

def import_data(database, directory_name, products_file, customers_file, rentals_file):
    """
    Takes a directory name and three csv files as input.
    Creates and populates three collections in MongoDB.
    :param db: MongoDB
    :return: List of tuples (one for customers and one for products).
    Each tuple contains:num of records processed, initial record count,
    final record count, and module run time
    """
    products = database["products"]
    customers = database["customers"]
    rentals = database["rentals"]
    results_dict = {}
    threads = [threading.Thread(target=add_bulk_data, args=(results_dict, products,
                                                            directory_name, products_file)),
               threading.Thread(target=add_bulk_data, args=(results_dict, customers,
                                                            directory_name, customers_file)),

               threading.Thread(target=add_bulk_data, args=(results_dict, rentals,
                                                            directory_name, rentals_file))]

    for thr in threads:
        thr.start()

    for thr in threads:
        thr.join()
    return [results_dict["customers"], results_dict["products"]]


def show_available_products(database):
    """
    Returns a dictionary for each product listed as available.    
    :return: Dictionary with product_id, description,
    product_type, quantity_available.
    """
    available_products = {}
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
    for product in database.products.find():
        if int(product["qantity_available"]) > 0:
            product_dict = {"description": product["description"],
                            "product_type": product["product_type"],
                            "quantity_available": product["qantity_available"]}
            available_products[product["product_id"]] = product_dict
    return available_products


def show_rentals(database, product_id):
    """
    Returns a dictionary with user information from
    users who have rented products matching the product_id.
    :return: user_id, name, address, phone_number, email
    """
    customer_info = {}
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
    for rental in database.rentals.find():

        if rental["product_id"] == product_id:

            customer_id = rental["user_id"]
            customer_record = database.customers.find_one({"Id": customer_id})
            customer_dict = {"Name": customer_record["Name"],

                             "address": customer_record["Home_address"],
                             "phone_number": customer_record["Phone_number"],

                             "email": customer_record["Email_address"]}
            customer_info[customer_id] = customer_dict            
    return customer_info


def clear_data(database):
    """
    Delete data in MongoDB.
    :return: Empty MongoDB.
    """
    database.products.drop()
    database.customers.drop()
    database.rentals.drop()

def main():
    """
    Main function
    :return: List of two tuples
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        results = import_data(database, "", "../data/product.csv",
                              "../data/customer.csv", "../data/rental.csv")
        clear_data(database)
    return results


if __name__ == "__main__":
    print(timeit("main()", globals=globals(), number=1))




