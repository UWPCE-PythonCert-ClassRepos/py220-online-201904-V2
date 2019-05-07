"""
Module for basic database operations
"""
# pylint: disable= W0614, W0401, R0913, W1203, W0612, W0703, E1111

import logging
from customer_model import *


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(
        customer_id,
        name,
        lastname,
        home_address,
        phone_number,
        email_address,
        status,
        credit_limit):
    '''
    This function will add a new customer to the  database.
    '''
    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                customer_name=name,
                customer_lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info(
                f'added {name} {lastname} successfully. ID = {customer_id}')
    except Exception as error:
        LOGGER.info(
            f'Error creating {name} {lastname} with ID = {customer_id}')


def search_customer(customer_id):
    """
    This function will search for a customer
    """
    LOGGER.info('Searching for customer')
    try:
        customer_verify = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info(f'customer with ID {customer_id} found')
        a_customer = {
            'name': customer_verify.customer_name,
            'lastname': customer_verify.customer_lastname,
            'email': customer_verify.email_address,
            'phone_number': customer_verify.phone_number
        }

    except Exception as error:
        LOGGER.info('Customer could not be found')
        return {}

    return a_customer


def delete_customer(customer_id):
    """
    This func. will delete a customer from the database
    """
    LOGGER.info('Deleting a customer')
    try:
        customer_delete = Customer.get(Customer.customer_id == customer_id)
        customer_delete.delete_instance()
        LOGGER.info(f'Customer with ID {customer_id} deleted')

    except Exception as error:
        LOGGER.info(f'Customer with ID {customer_id} not deleted')


def update_customer_credit(customer_id, credit_limit):
    """
    This method updates the customers credit
    """
    update_credit = Customer.update(credit_limit=credit_limit).where(
        Customer.customer_id == customer_id)
    LOGGER.info(
        f'Raised credit limit to {credit_limit} for ID = {customer_id}')
    if not update_credit.execute():
        raise ValueError("NoCustomer")


def list_active_customers():
    '''
    This function counts the number of active customers
    '''
    count = 0
    try:
        LOGGER.info('Counting active customers')
        query = (Customer.select(Customer.customer_id, Customer.status)
                 .where(Customer.status == 'active'))
        count = query.select().count()
    except Exception as error:
        LOGGER.info('Customer does not exist')

    return count
