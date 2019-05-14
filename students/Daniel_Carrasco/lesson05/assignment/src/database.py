""""
Lesson 5. Create DB using mongodb api
"""

from pymongo import MongoClient #high level api
import glob
import logging
import csv

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler('db.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)



logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


class MongoDBConnection(object):
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

def read_data(directory_name,file_name):
    logger.info(f'reading {file_name} data from {directory_name}')
    data_list = []
    try:
        with open(directory_name+file_name) as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader, None)
            header[0]=header[0].replace("\ufeff","")

            for row in reader:
                temp_dict={}
                for index, value in enumerate(header):
                    temp_dict[value] = row[index]
                data_list.append(temp_dict)
    except Exception as error:
        logger.info(f'could not read data due to {error}')
    return data_list


def import_data(directory_name, product_file, customer_file, rentals_file):
    logger.info("importing data")
    product_ip = read_data(directory_name,product_file)
    customer_ip = read_data(directory_name,customer_file)
    rentals_ip = read_data(directory_name,rentals_file)

    return product_ip, customer_ip, rentals_ip

def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)




def main():
    logger.info("starting MongoDBConnection")
    mongo = MongoDBConnection()

    with mongo:

        # mongodb database; it all starts here
        db = mongo.connection.HPNorton
        product_ip, customer_ip, rentals_ip = import_data("../data/", "product.csv", "customers.csv", "rental.csv")

        # collection in database
        products = db["product"]
        customers = db["customers"]
        rentals = db["rental"]

        product_results = products.insert_many(product_ip)
        print_mdb_collection(products)
        customer_results = customers.insert_many(customer_ip)
        print_mdb_collection(customers)
        rental_results = rentals.insert_many(rentals_ip)
        print_mdb_collection(rentals)
        """


        # related data
        for name in collector.find():
            print(f'List for {name["name"]}')
            query = {"name": name["name"]}
            for a_cd in cd.find(query):
                print(f'{name["name"]} has collected {a_cd}')


        # start afresh next time?
        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            cd.drop()
            collector.drop()
            """


if __name__== "__main__":
    main()

