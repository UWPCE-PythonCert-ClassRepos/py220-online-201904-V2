""""
Initialization of Mongodb connection
"""
import os
from pymongo import MongoClient
from contextlib import contextmanager


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


def query_products(col):
    """
    Query quantity available
    """

    query_is_available = {"quantity_available": {"$gt": 0}}
    return col.find(query_is_available)


def query_rentals(col_cust, col_prod, col_rent):
    """
    Query rentals
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
    Find collection name
    """
    for doc in collection_name.find():
        print(doc)


@contextmanager
def mongo_context():
    """
    Mongo context manager
    """
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        yield db


def main():
    """
    Run program in main
    """

    with mongo_context() as db:

        # customer.csv
        db_cust = db["customers"]
        db_cust.drop()
        db_cust_data = list()
        with open(os.path.join('data', 'customers.csv'), 'r') as f:
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
        print_mdb_collection(db_cust)
        print("")

        # product.csv
        db_prod = db["product"]
        db_prod.drop()
        db_prod_data = list()
        with open(os.path.join('data', 'product.csv'), 'r') as f:
            for line in f.readlines()[1:]:
                record = line.rstrip('\n').split(',')
                if len(record) == 4:
                    # product_id,description,product_type,quantity_available
                    db_prod_data.append({"product_id":         record[0],
                                         "description":        record[1],
                                         "product_type":       record[2],
                                         "quantity_available": int(record[3])})
        db_prod.insert_many(db_prod_data)
        print_mdb_collection(db_prod)
        print("")

        # rental.csv
        db_rent = db["rental"]
        db_rent.drop()
        db_rent_data = list()
        with open(os.path.join('data', 'rental.csv'), 'r') as f:
            for line in f.readlines()[1:]:
                record = line.rstrip('\n').split(',')
                if len(record) == 2:
                    # product_id,user_id
                    db_rent_data.append({"product_id": record[0],
                                         "user_id":    record[1]})
        db_rent.insert_many(db_rent_data)
        print_mdb_collection(db_rent)
        print("")

        # Query all available products
        products_available = query_products(db_prod)
        for p in products_available:
            print('%s (%s available): %s' %
                  (p['product_id'], p['quantity_available'], p['description']))
        print("")

        # Query customer and product data
        rentals = query_rentals(db_cust, db_prod, db_rent)
        for rental in rentals:
            print(rental)
        print("")


if __name__ == '__main__':
    main()
