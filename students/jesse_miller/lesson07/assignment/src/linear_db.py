import csv
import os
import time
from timeit import timeit
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


def _import_csv(filename):
    '''
    Returns a list of dictionaries.  One dictionary for each row of data in a
    csv file.
    '''

    with open(filename, newline='') as csvfile:
        dict_list = []

        csv_data = csv.reader(csvfile)

        headers = next(csv_data, None)  # Save the first line as the headers

        if headers[0].startswith('ï»¿'):  # Check for weird formatting
            headers[0] = headers[0][3:]

        for row in csv_data:
            row_dict = {column: row[index] for index, column in enumerate(headers)}

            dict_list.append(row_dict)

        return dict_list


def _add_bulk_data(collection, directory_name, filename):
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

    return records_processed, initial_records, final_records, run_time


def import_data(db, directory_name, products_file, customers_file, rentals_file):
    '''
    Takes a directory name and three csv files as input.  Creates and populates
    three collections in MongoDB.
    '''

    products = db['products']
    products_results = _add_bulk_data(products, directory_name, products_file)

    customers = db['customers']
    customers_results = _add_bulk_data(customers, directory_name, customers_file)

    rentals = db['rentals']
    _add_bulk_data(rentals, directory_name, rentals_file)

    return [customers_results, products_results]


def show_available_products(db):
    '''
    Returns a dictionary for each product listed as available.
    '''

    available_products = {}

    for product in db.products.find():
        if product['quantity_available'] != '0':
            short_dict = {key: value for key, value in product.items() if key \
            not in ('_id', 'product_id')}
            available_products[product['product_id']] = short_dict

    return available_products


def show_rentals(db, product_id):
    '''
    Returns a dictionary with user information from users who have rented
    products matching the product_id.
    '''

    customer_info = {}

    for rental in db.rentals.find():
        if rental['product_id'] == product_id:
            customer_id = rental['user_id']
            customer_record = db.customers.find_one({'user_id': customer_id})

            short_dict = {key: value for key, value in customer_record.items() \
            if key not in ('_id', 'user_id')}
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
        db = mongo.connection.media

        results = import_data(db, '', 'product.csv', 'customer.csv', 'rental.csv')

        clear_data(db)

    return results


if __name__ == '__main__':
    main()
    print(timeit('main()', globals=globals(), number=1))
    print(timeit('main()', globals=globals(), number=10))
