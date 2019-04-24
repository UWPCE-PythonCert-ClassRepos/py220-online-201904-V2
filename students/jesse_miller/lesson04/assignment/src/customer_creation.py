#!/usr/bin/env python3
"""
Create a customers database for Norton.
"""
import logging
import customer_schema as schema

def main():
    '''
    A simple table creation for our database using customer_schema.py
    '''
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    log_file = logging.FileHandler('db.log')
    log_file.setLevel(logging.DEBUG)

    log_format = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d\
%(levelname)s %(message)s')

    log_file.setFormatter(log_format)

    logger.addHandler(log_file)
    log_stream = logging.StreamHandler()
    log_stream.setLevel(logging.DEBUG)
    log_stream.setFormatter(log_format)

    logger.info('Creating a database using the customer schema.')
    schema.database.create_tables([schema.Customer])
    schema.database.close()
