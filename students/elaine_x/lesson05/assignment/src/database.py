""""
must use 127.0.0.1 on windows
pip install pymongo

"""
import csv
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def read_csv(path):
    '''
    read in csv as a list
    '''
    with open(path, 'r', encoding='utf-8-sig') as file:
        readcsv = csv.reader(file, delimiter=',')
        data_list = []
        iterator = iter(readcsv)
        key = []
        row1 = next(iterator)
        for item in row1:
            key.append(str(item))
        while True:
            try:
                row = next(iterator)
                formatted_row = {}
                for i, item in enumerate(row):
                    formatted_row[key[i]] = item
                #LOGGER.info('print %s', formatted_row)
                data_list.append(formatted_row)
            except StopIteration:
                LOGGER.info('Stop Iteration')
                break
            except UnicodeDecodeError as error_message:
                LOGGER.info('Error reading')
                LOGGER.info(error_message)
    return data_list


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


def print_mdb_collection(collection_name):
    '''print database to screen'''
    for doc in collection_name.find():
        print(doc)


def import_data(path, prod_file, cust_file, rental_file):
    '''import data to mangodb'''
    #read from csv
    customers = read_csv(path + cust_file)
    product = read_csv(path + prod_file)
    rental = read_csv(path + rental_file)

    #connect to mongo
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        d_b = mongo.connection.media

        # collection in database
        cdb = d_b["customers"]
        #cdb.insert_many(customers)
        cust_iterator = iter(customers)
        i = 0
        err_i = 0
        while True:
            try:
                entry = next(cust_iterator)
                cdb.insert_one(entry)
                i += 1
                #LOGGER.info('i = %s', i)
            except StopIteration:
                LOGGER.info('Stop Iteration')
                break
            except Exception:
                err_i += 1
                LOGGER.info('err_i = %s', err_i)
        print_mdb_collection(cdb)

        pdb = d_b["product"]
        #pdb.insert_many(product)
        prod_iterator = iter(product)
        j = 0
        err_j = 0
        while True:
            try:
                entry = next(prod_iterator)
                pdb.insert_one(entry)
                j += 1
                #LOGGER.info('j = %s', j)
            except StopIteration:
                LOGGER.info('Stop Iteration')
                break
            except Exception:
                err_j += 1
                LOGGER.info('err_j = %s', err_j)
        print_mdb_collection(pdb)

        rtdb = d_b["rental"]
        #rtdb.insert_many(rental)
        rental_iterator = iter(rental)
        k = 0
        err_k = 0
        while True:
            try:
                entry = next(rental_iterator)
                rtdb.insert_one(entry)
                k += 1
                #LOGGER.info('k = %s', k)
            except StopIteration:
                LOGGER.info('Stop Iteration')
                break
            except Exception:
                err_k += 1
                LOGGER.info('err_k = %s', err_k)
        print_mdb_collection(rtdb)

    return (i, j, k), (err_i, err_j, err_k)


def show_available_products():
    '''show all available product in a dict'''
    mongo = MongoDBConnection()
    with mongo:
        d_b = mongo.connection.media
        pdb = d_b["product"]
        prod_dict = {}
        for entry in pdb.find():
            prod_dict[entry['product_id']] = {
                'description': entry['description'],
                'product_type': entry['product_type'],
                'quantity_available': entry['quantity_available']}
    return prod_dict


def show_rentals(product_id):
    '''show all customers that have rented the product'''
    mongo = MongoDBConnection()
    with mongo:
        d_b = mongo.connection.media
        rtdb = d_b["rental"]
        cdb = d_b["customers"]
        cust_dict = {}
        query = {'product_id': product_id}
        for a_rtdb in rtdb.find(query):
            #LOGGER.info(a_rtdb)
            query2 = {'user_id': a_rtdb['user_id']}
            for a_cbd in cdb.find(query2):
                cust_dict[a_cbd['user_id']] = {
                    'name': a_cbd['name'],
                    'address': a_cbd['address'],
                    'phone_number': a_cbd['phone_number'],
                    'email': a_cbd['email']}
    return cust_dict


def drop_data():
    '''start afresh next time?'''
    mongo = MongoDBConnection()
    with mongo:
        d_b = mongo.connection.media
        cdb = d_b["customers"]
        pdb = d_b["product"]
        rtdb = d_b["rental"]
        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            cdb.drop()
            pdb.drop()
            rtdb.drop()


if __name__ == "__main__":
    print(import_data('../data/', "product.csv", "customers.csv", "rental.csv"))
    print(show_available_products())
    print(show_rentals('prd002'))
    drop_data()
