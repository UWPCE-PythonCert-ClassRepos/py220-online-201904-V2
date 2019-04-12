#!/usr/bin/env python3
"""
    Imports customer.csv to sqlite database
"""

import csv
import logging
from db_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Initializes the HP Norton database")

database.create_tables([Customer])

CUSTOMER_ID = 0
NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
STATUS = 6
CREDIT_LIMIT = 7

filename = './customer.csv'
content = open(filename, 'rb').read().decode('utf-8', errors='ignore')
lines = content.split('\n')

for line in lines:
    customer = line.split(',')
    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer[CUSTOMER_ID],
                name=customer[NAME],
                last_name=customer[LAST_NAME],
                home_address=customer[HOME_ADDRESS],
                phone_number=customer[PHONE_NUMBER],
                email_address=customer[EMAIL_ADDRESS],
                status=customer[STATUS],
                credit_limit=customer[CREDIT_LIMIT],
            )
            logger.info(f"Adding record for {customer[CUSTOMER_ID]}")
    except Exception as ex:
        logger.info(ex)

database.close()
