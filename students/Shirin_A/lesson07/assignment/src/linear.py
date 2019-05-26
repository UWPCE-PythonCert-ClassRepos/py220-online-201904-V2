"""
HP Norton MongoDB Project
Uses Pymongo to access MongoDB database
"""
import csv
import os
import time
from timeit import timeit
import pymongo

# pylint: disable= C0303

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
    Prints documents in a collection.    
    """
    for doc in collection_name.find():
        print(doc)
        

def _import_csv(filename):
    """
    Returns a list of dictionaries.One dictionary
    for each row of data in a csv file.
    :return: list of dictionaries
    """
    
    with open(filename, newline="") as csvfile:
        dict_list = []
        csv_data = csv.reader(csvfile)
        headers = next(csv_data, None)  
        if headers[0].startswith("ï»¿"): 
            headers[0] = headers[0][3:]
        for row in csv_data:
            row_dict = {}
            for index, column in enumerate(headers):
                row_dict[column] = row[index]
            dict_list.append(row_dict)
        return dict_list


def _add_bulk_data(collection, directory_name, filename):

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
    collection.insert_many(_import_csv(file_path), ordered=False)
    final_records = collection.count_documents({})

    records_processed = final_records - initial_records
    run_time = time.time() - start_time
    return records_processed, initial_records, final_records, run_time


def import_data(database, directory_name, products_file, customers_file, rentals_file):
    """
    Takes a directory name and three csv files as input.
    Creates and populates a new MongoDB.
    :return:List of tuples (one for customers and one for products).
    Each tuple contains:num of records processed, initial record count,
    final record count, and module run time 
    """
    products = database["products"]
    products_result = _add_bulk_data(products, directory_name, products_file)
    customers = database["customers"]
    customers_result = _add_bulk_data(customers, directory_name, customers_file)

    rentals = database["rentals"]
    _add_bulk_data(rentals, directory_name, rentals_file)
    return products_result, customers_result


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



def clear_data(database):
    """
    Delete data in MongoDB.
    :return: Empty MongoDB.
    """
    database.products.drop()
    database.customers.drop()
    database.rentals.drop()
    
            
if __name__ == "__main__":
    print(timeit("main()", globals=globals(), number=1))


   
