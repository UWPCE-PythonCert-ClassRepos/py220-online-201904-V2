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
    header = ['customer_id', 'name', 'last_name', 'home_address', 'phone_number',
              'email_address', 'status', 'credit_limit']
    try:
        with open("customer.csv", 'r') as f:
            customer_list = csv.DictReader(f, fieldnames=header, delimiter=',')
            next(customer_list)  # omit the header line
            for person in customer_list:
                person['credit_limit'] = int(person['credit_limit'])  # change the type to int
                try:
                    with DB.transaction():
                        Customer.create(**person).save()
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
