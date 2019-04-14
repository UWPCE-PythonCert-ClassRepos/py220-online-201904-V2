#!/usr/bin/env python3
"""
    Imports customer.csv to sqlite database
"""

# Execution time for seeding the database: 293.8888795375824 seconds.
# System: Linux Mint 19, Core i7-6700k at 4.4GHz, 32GB DDR4, NVME2 Drive
# CPU usage was only around 5-6% for the process.
# I feel like it should have at least maxed one core and done this
#   much more quickly, they're more than enough RAM / CPU power.
#   Why is this bottlenecked so badly?


import logging
import time
from db_model import *

start = time.time()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Initializes the HP Norton database from csv")
filename = "../data/head-cust.csv"
database.create_tables([Customer])

CUSTOMER_ID = 0
NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
STATUS = 6
CREDIT_LIMIT = 7

with open(filename, "rb") as content:
    next(content)  # Skip first line, it's the column names
    lines = content.read().decode("utf-8", errors="ignore").split("\n")
    for line in lines:
        customer = line.split(",")
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
        except IndexError:
            logger.info("End of file")

logger.info(f"Time to init: {time.time() - start}")
database.close()
