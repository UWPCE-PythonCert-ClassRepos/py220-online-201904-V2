""""
Timing functions to show profile performance
"""
import argparse
import os
from timeit import default_timer as timer
import datetime as dt
from pymongo import MongoClient

timing_filename = 'out.txt'


def timing_wrapper(func):
    """ 
    Timing decorator
    """
    def inner(*args, **kwargs):
        start = timer()
        result = func(*args, **kwargs)
        stop = timer()
        with open(timing_filename, 'a') as fout:
            fout.write('Function: %s , Time: %s , Records Processed: %s\n' % (func.__name__,
                                                                              dt.timedelta(
                                                                                  seconds=stop-start),
                                                                              len(list(result))))
        return result
    return inner


def parse_cmd_arguments():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description='Read data files.')
    parser.add_argument('-c', '--customer',
                        help='customer data file', required=True)
    parser.add_argument('-p', '--product',
                        help='product data file', required=True)
    parser.add_argument(
        '-r', '--rental', help='rental data file', required=True)
    parser.add_argument(
        '-o', '--output', help='output text file', required=True)

    return parser.parse_args()


class MongoDBConnection():
    """ 
    MongoDB Connection
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


@timing_wrapper
def query_products(col):
    """
    Return Products found
    """
    query_is_available = {"quantity_available": {"$gt": 0}}
    return col.find(query_is_available)


@timing_wrapper
def query_rentals(col_cust, col_prod, col_rent):
    """
    Return customer data
    """
    return_data = []
    for e in col_rent.find():
        cust = col_cust.find_one({"user_id": e["user_id"]})
        prod = col_prod.find_one({"product_id": e["product_id"]})
        return_data.append('Customer %s rented %s.' %
                           (cust['name'], prod['description']))
    return return_data


def print_mdb_collection(collection_name):
    """
    Return collection names
    """
    for doc in collection_name.find():
        print(doc)


def main():
    """
    Runs program in main
    """

    args = parse_cmd_arguments()

    global timing_filename
    timing_filename = args.output
    if os.path.isfile(timing_filename):
        os.remove(timing_filename)

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.media

        # customer.csv
        db_cust = db["customers"]
        db_cust.drop()
        db_cust_data = list()
        with open(args.customer, 'r', encoding="utf8", errors='ignore') as f:
            for line in f.readlines()[1:]:
                record = line.rstrip('\n').split(',')
                if len(record) == 6:
                    # user_id,name,address,zip_code,phone_number,email
                    db_cust_data.append({"user_id":      record[0],
                                         "name":         record[1],
                                         "address":      record[2],
                                         "zip_code":     record[3],
                                         "phone_number": record[4],
                                         "email":        record[5]})
        db_cust.insert_many(db_cust_data)

        print('Read customer data.')

        # product.csv
        db_prod = db["product"]
        db_prod.drop()
        db_prod_data = list()
        with open(args.product, 'r', encoding="utf8", errors='ignore') as f:
            for line in f.readlines()[1:]:
                record = line.rstrip('\n').split(',')
                if len(record) == 4:
                    # product_id,description,product_type,quantity_available
                    db_prod_data.append({"product_id":         record[0],
                                         "description":        record[1],
                                         "product_type":       record[2],
                                         "quantity_available": int(record[3])})
        db_prod.insert_many(db_prod_data)

        print('Read product data.')

        # rental.csv
        db_rent = db["rental"]
        db_rent.drop()
        db_rent_data = list()
        with open(args.rental, 'r', encoding="utf8", errors='ignore') as f:
            for line in f.readlines()[1:]:
                record = line.rstrip('\n').split(',')
                if len(record) == 2:
                    # product_id,user_id
                    db_rent_data.append({"product_id": record[0],
                                         "user_id":    record[1]})
        db_rent.insert_many(db_rent_data)

        print('Read rental data.')

        print('Queried available products.')

        print('Queried rentals.')


if __name__ == '__main__':
    main()
