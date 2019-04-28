"""
    Learning persistence with Peewee and sqlite
    Add customers from csv
        (but running this program does not require it)


"""

import csv
import logging
from peewee import *
from customer_model import Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Working with Person class')
LOGGER.info('Note how I use constants and a list of tuples as a simple schema')
LOGGER.info('Normally you probably will have prompted for this from a user')

DATABASE = SqliteDatabase('customer.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

with open('../data/customer.csv', 'r') as f:
    READCSV = csv.reader(f, delimiter=',')
    CUSTOMERS = []
    try:
        for i, row in enumerate(READCSV):
            #LOGGER.info(f'print {row}')
            CUSTOMERS.append(row)
    except UnicodeDecodeError as error_message:
        LOGGER.info('Error reading = %sth row', i)
        LOGGER.info(error_message)


CUSTOMER_ID = 0
CUSTOMER_NAME = 1
CUSTOMER_LASTNAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
STATUS = 6
CREDIT_LIMIT = 7


LOGGER.info('Creating Customer records: iterate through the list of tuples')
LOGGER.info('Prepare to explain any errors with exceptions')
LOGGER.info('and the transaction tells the database to rollback on error')

for customer in CUSTOMERS:
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                customer_id=customer[CUSTOMER_ID],
                customer_name=customer[CUSTOMER_NAME],
                customer_lastname=customer[CUSTOMER_LASTNAME],
                home_address=customer[HOME_ADDRESS],
                phone_number=customer[PHONE_NUMBER],
                email_address=customer[EMAIL_ADDRESS],
                status=customer[STATUS],
                credit_limit=customer[CREDIT_LIMIT]
                )
            new_customer.save()
            #LOGGER.info('Database add successful')

    # it was giving me model based error type,
    # not sure what error type would work here?
    except Exception as error_message:
        LOGGER.info('Error creating = %s', customer[CUSTOMER_ID])
        LOGGER.info(error_message)
        LOGGER.info('See how the database protects our data')

DATABASE.close()
