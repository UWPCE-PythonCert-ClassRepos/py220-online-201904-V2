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

    logger.info('Creating a database using the customer schema.')

    schema.database.create_tables([
        schema.Customer
    ])

    schema.database.close()
