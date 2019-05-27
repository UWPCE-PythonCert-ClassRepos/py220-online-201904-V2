""""
must use 127.0.0.1 on windows
pip install pymongo

"""
import csv
import logging
import time
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


def import_data(path, prod_file, cust_file):
    '''import data to mangodb'''

    #connect to mongo
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        d_b = mongo.connection.media
        start1 = time.time()
        # read from csv
        customers = read_csv(path + cust_file)
        # collection in database
        cdb = d_b["customers"]
        count_prior_i = cdb.count()
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
        count_after_i = cdb.count()
        #print_mdb_collection(cdb)
        end1 = time.time()
        time1 = end1 - start1

        start2 = time.time()
        product = read_csv(path + prod_file)

        pdb = d_b["product"]
        count_prior_j = pdb.count()
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
        count_after_j = pdb.count()
        #print_mdb_collection(pdb)
        end2 = time.time()

        time2 = end2 - start2

    #rental = read_csv(path + rental_file)
    #with mongo:
        ## mongodb database; it all starts here
        #d_b = mongo.connection.media
        #rtdb = d_b["rental"]
        ##rtdb.insert_many(rental)
        #rental_iterator = iter(rental)
        #k = 0
        #err_k = 0
        #while True:
            #try:
                #entry = next(rental_iterator)
                #rtdb.insert_one(entry)
                #k += 1
                ##LOGGER.info('k = %s', k)
            #except StopIteration:
                #LOGGER.info('Stop Iteration')
                #break
            #except Exception:
                #err_k += 1
                #LOGGER.info('err_k = %s', err_k)
        ##print_mdb_collection(rtdb)

    return (i, count_prior_i, count_after_i, time1), \
           (j, count_prior_j, count_after_j, time2)


#def show_available_products():
    #'''show all available product in a dict'''
    #mongo = MongoDBConnection()
    #with mongo:
        #d_b = mongo.connection.media
        #pdb = d_b["product"]
        #prod_dict = {}
        #for entry in pdb.find():
            #prod_dict[entry['product_id']] = {
                #'description': entry['description'],
                #'product_type': entry['product_type'],
                #'quantity_available': entry['quantity_available']}
    #return prod_dict


#def show_rentals(product_id):
    #'''show all customers that have rented the product'''
    #mongo = MongoDBConnection()
    #with mongo:
        #d_b = mongo.connection.media
        #rtdb = d_b["rental"]
        #cdb = d_b["customers"]
        #cust_dict = {}
        #query = {'product_id': product_id}
        #for a_rtdb in rtdb.find(query):
            ##LOGGER.info(a_rtdb)
            #query2 = {'user_id': a_rtdb['user_id']}
            #for a_cbd in cdb.find(query2):
                ##LOGGER.info(a_cbd)
                #cust_dict[a_cbd['user_id']] = {
                    #'name': a_cbd['Name'],
                    #'last name': a_cbd['Last_name'],
                    #'home address': a_cbd['Home_address'],
                    #'phone_number': a_cbd['Phone_number'],
                    #'email': a_cbd['Email_address']}
    #return cust_dict


def drop_data():
    '''start afresh next time?'''
    mongo = MongoDBConnection()
    with mongo:
        d_b = mongo.connection.media
        cdb = d_b["customers"]
        pdb = d_b["product"]
        #rtdb = d_b["rental"]
        #yorn = input("Drop data?")
        #if yorn.upper() == 'Y':
        cdb.drop()
        pdb.drop()
        #rtdb.drop()


if __name__ == "__main__":
    print(import_data('../data/', "product.csv", "customer.csv"))
    #print(show_available_products())
    #print(show_rentals('P000003'))
    drop_data()
