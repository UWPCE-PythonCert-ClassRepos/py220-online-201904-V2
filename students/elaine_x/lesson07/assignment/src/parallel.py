""""
must use 127.0.0.1 on windows
pip install pymongo

"""

#import csv
import logging
import time
import threading
import math
from linear import MongoDBConnection, read_csv, drop_data
#from pymongo import MongoClient
THREAD_COUNT = 10

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def insert_data(table, csv_data, start, batch_size):
    '''insert data to dababase'''
    table.insert_many(csv_data[start:min(len(csv_data), start+batch_size)])


def import_table(table, path):
    '''import data to database thru threading'''
    csv_data = read_csv(path)
    group_size = math.ceil(len(csv_data) / THREAD_COUNT)
    threads = []
    for i in range(THREAD_COUNT):
        thread = threading.Thread(target=insert_data,
                                  args=(table,
                                        csv_data,
                                        group_size*i,
                                        group_size))
        threads.append(thread)
        thread.start()
    for i in range(THREAD_COUNT):
        threads[i].join()
    return len(csv_data)


def import_data(path, prod_file, cust_file):
    '''import data to mongodb'''
    #connect to mongo
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        d_b = mongo.connection.media

        #import customer data
        start1 = time.time()
        cdb = d_b["customers"]
        count_prior_i = cdb.count()
        customer_entry = import_table(cdb, path + cust_file)
        count_after_i = cdb.count()
        #print_mdb_collection(cdb)
        end1 = time.time()
        time1 = end1 - start1

        #import Product Data
        start2 = time.time()
        pdb = d_b["product"]
        count_prior_j = pdb.count()
        product_entry = import_table(pdb, path + prod_file)
        count_after_j = pdb.count()
        #print_mdb_collection(pdb)
        end2 = time.time()
        time2 = end2 - start2
    return (customer_entry, count_prior_i, count_after_i, time1), \
           (product_entry, count_prior_j, count_after_j, time2)


if __name__ == "__main__":
    print(import_data('../data/', "product.csv", "customer.csv"))
    drop_data()
