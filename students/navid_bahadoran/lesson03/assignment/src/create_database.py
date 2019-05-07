# pylint: disable=W0401, R0903, C0103, W1203, W0614, E0602, E0401
""" This file create a HPNorton.db database from the customer.csv file"""
import csv
import logging
from peewee import IntegrityError
from .model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def create_table():
    """create table"""
    DB.create_tables([Customer])


def populate_data():
    """ Populate data"""
    try:
        with open("customer.csv", 'r') as f:
            customer_list = csv.reader(f, delimiter=',')  # read data from customer.csv file
            header = next(customer_list)  # separate the header from the other data
            header = [i.lower() for i in header]  # adjust the header item to the the/
            # field name of our table
            header[0] = "customer_" + header[0]  # adjust the header item to the the/
            # field name of our table
            for person in customer_list:
                customer_item = dict(zip(header, person))
                try:
                    with DB.transaction():
                        Customer.create(**customer_item).save()

                        # logger.info(f"Record for customer Id:{person[0]} was added successfully")
                except IntegrityError:
                    LOGGER.info("There is duplicate in the entry")
    except IOError as error:
        LOGGER.info(f"there is issue in opening a file{error}")


def main():
    """ main function"""
    create_table()
    populate_data()


if __name__ != '__main__':
    main()
    DB.close()
