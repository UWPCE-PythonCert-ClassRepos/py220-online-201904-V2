#!/usr/bin/env python3
'''
Lesson 3, learning database operations.
'''
import logging
import peewee
import customer_creation as cc
import customer_schema as cs

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

logging.info('Starting basic operations for customer database.')

# pylint: disable = R0913
def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, active_status, credit_limit):
    '''
    Adding a new customer to the DB
    '''
    try:
        new_customer = cs.Customer.create(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            active_status=active_status,
            credit_limit=credit_limit)
        new_customer.save()
        logging.info('Successfully added %s %s to the database.', first_name, \
        last_name)

    except peewee.IntegrityError as add_error:
        logging.error("%s. Error adding %s %s to the database.", add_error, \
        first_name, last_name)
        raise peewee.IntegrityError

def delete_customer():
    '''
    Deleting a customer from the DB
    '''
    pass

def search_customer():
    '''
    Search DB for an active customer
    '''
    pass

def list_active_customers():
    '''
    List all active customers
    '''
    pass

def update_customer_credit():
    '''
    Update customer credit limits
    '''
    pass
