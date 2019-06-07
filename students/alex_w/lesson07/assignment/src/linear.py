import os
import queue
import threading
import timeit
from pymongo import MongoClient



class MongoDBConnection():
    """MongoDB Connection"""

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


def import_customers():
    db_cust_data = list()
    with open(os.path.join('data', 'customer.csv'), 'r') as f:
        for line in f.readlines()[1:]:
            record = line.rstrip('\n').split(',')
            if len(record) == 8:
                """ user_id,name,address,zip_code,phone_number,email """
                db_cust_data.append({"user_id": record[0],
                                     "name": record[1],
                                     "last_name": record[2],
                                     "address": record[3],
                                     "phone_number": record[4],
                                     "email": record[5],
                                     "status": record[6],
                                     "credit_limit": record[7]})
    """ print("finished customers") """
    return db_cust_data


def import_product():
    db_prod_data = list()
    with open(os.path.join('data', 'product.csv'), 'r') as f:
        for line in f.readlines()[1:]:
            record = line.rstrip('\n').split(',')
            if len(record) == 4:
                """ product_id,description,product_type,quantity_available """
                db_prod_data.append({"product_id": record[0],
                                     "description": record[1],
                                     "product_type": record[2],
                                     "quantity_available": int(record[3])})
    """ print("finished product") """
    return db_prod_data


def import_rental():
    db_rent_data = list()
    with open(os.path.join('data', 'rental.csv'), 'r') as f:
        for line in f.readlines()[1:]:
            record = line.rstrip('\n').split(',')
            if len(record) == 6:
                """ product_id,user_id """
                db_rent_data.append({"user_id": record[0],
                                     "name": record[1],
                                     "address": record[2],
                                     "phone_number": record[3],
                                     "email": record[4],
                                     "product_id": record[5]})
    """ print("finished rental") """
    return db_rent_data


def import_all_data(db):

    db_cust = db["customers"]
    db_rent = db["rental"]
    db_prod = db["product"]

    """ reading customers, product, and rental data """
    records_cust = import_customers()
    records_prod = import_product()
    records_rent = import_rental()

    """ insert data into the database """
    db_cust.insert_many(records_cust)
    db_prod.insert_many(records_prod)
    db_rent.insert_many(records_rent)

    """ return the number of records processed for each data set """
    return {'customers': len(records_cust),
            'product': len(records_prod),
            'rental': len(records_rent)}


def main():

    """ start main module timer """
    start = timeit.default_timer()

    mongo = MongoDBConnection()
    with mongo:

        """ initialize database """
        db = mongo.connection.media
        db_cust = db["customers"]
        db_rent = db["rental"]
        db_prod = db["product"]

        """ empty the collections """
        db_cust.drop()
        db_rent.drop()
        db_prod.drop()

        """ count the number of initial documents in the collection """
        num_initial_customers = db_cust.count_documents({})
        num_initial_rental = db_rent.count_documents({})
        num_initial_product = db_prod.count_documents({})

        """ import all the data, and return dictionary of number of records processed """
        num_processed = import_all_data(db)

        """ count the number of final documents in the collection """
        num_final_customers = db_cust.count_documents({})
        num_final_rental = db_rent.count_documents({})
        num_final_product = db_prod.count_documents({})

    """ end main module timer """
    end = timeit.default_timer()

    """ create tuples required by the assignment """
    tuple_customers = (num_processed['customers'], num_initial_customers, num_final_customers, end-start)
    tuple_rental = (num_processed['rental'], num_initial_rental, num_final_rental, end-start)
    tuple_product = (num_processed['product'], num_initial_product, num_final_product, end-start)

    """ display the tuples and return them """
    print("Customers tuple:")
    print(tuple_customers)
    print("Rental tuple:")
    print(tuple_rental)
    print("Product tuple:")
    print(tuple_product)
    print('')
    return tuple_customers, tuple_rental, tuple_product


if __name__ == '__main__':

    num_replications = 5
    timing = timeit.timeit("main()", setup="from __main__ import main", number=num_replications)
    print('Average runtime (secs) of linear version: %s' % str(round(timing/float(num_replications),2)))
