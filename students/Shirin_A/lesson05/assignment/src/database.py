"""
HP Norton MongoDB Project
Uses Pymongo to access MongoDB database
"""
import csv
import os
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
    If it works properly, it will handle the
    bulk imports from the csv files
    """
    file_path = os.path.join(directory_name, filename)
    try:
        collection.insert_many(_import_csv(file_path), ordered=False)

        return 0
    except pymongo.errors.BulkWriteError as bwe:

        print(bwe.details)
        return len(bwe.details["writeErrors"])


def import_data(database, directory_name, products_file, customers_file, rentals_file):
    """
    Takes a directory name and three csv files as input.
    Creates and populates a new MongoDB.
    :return: Tuple with record count for products, customers,
    rentals added (in that order) and
    tuple with count of errors that occurred for products,
    customers, rentals (in that order).
    """

    mongo = MongoDBConnection()
    with mongo:

        database = mongo.connection.media

    products = database["products"]
    products_errors = _add_bulk_data(products, directory_name, products_file)
    customers = database["customers"]
    customers_errors = _add_bulk_data(customers, directory_name, customers_file)

    rentals = database["rentals"]
    rentals_errors = _add_bulk_data(rentals, directory_name, rentals_file)

    record_count = (database.products.count_documents({}), database.customers.count_documents({}),
                    database.rentals.count_documents({}))
    error_count = (products_errors, customers_errors, rentals_errors)
    return record_count, error_count

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
        if int(product["quantity_available"]) > 0:
            product_dict = {"description": product["description"],
                            "product_type": product["product_type"],
                            "quantity_available": product["quantity_available"]}
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
            customer_record = database.customers.find_one({"user_id": customer_id})
            customer_dict = {"name": customer_record["name"],

                             "address": customer_record["address"],
                             "phone_number": customer_record["phone_number"],

                             "email": customer_record["email"]}
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



if __name__ == "__main__":

    MONGO = MongoDBConnection()
    with MONGO:
        print("Opening a MongoDB.\n")
        DATABASE = MONGO.connection.media
        print("Importing data for products, customers, and rentals.\n")
        import_data(DATABASE, "../data", "../data/product.csv", "../data/customers.csv",
                    "../data/rental.csv")
        print("Showing available products:")
        print(show_available_products(DATABASE))
        print("\nShowing rental information for prd005:")
        print(show_rentals(DATABASE, "prd005"))
        print("\nClearing data from database.")
        clear_data(DATABASE)
