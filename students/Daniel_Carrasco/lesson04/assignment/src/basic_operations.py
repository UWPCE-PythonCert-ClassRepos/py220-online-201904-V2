"""
Module for basic database operations
"""
# pylint: disable= W0614, W0401, R0913, W1203, W0612, W0703, E1111

import logging
from customer_model import *


log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler('db.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)



logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)



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
            logger.info(
                f'added {name} {lastname} successfully. ID = {customer_id}')
    except Exception as error:
        logger.info(
            f'Error creating {name} {lastname} with ID = {customer_id}')


def search_customer(customer_id):
    """
    This function will search for a customer
    """
    logger.info('Searching for customer')
    try:
        customer_verify = Customer.get(Customer.customer_id == customer_id)
        logger.info(f'customer with ID {customer_id} found')
        a_customer = {
            'name': customer_verify.customer_name,
            'lastname': customer_verify.customer_lastname,
            'email': customer_verify.email_address,
            'phone_number': customer_verify.phone_number
        }

    except Exception as error:
        logger.info('Customer could not be found')
        return {}

    return a_customer


def delete_customer(customer_id):
    """
    This func. will delete a customer from the database
    """
    logger.info('Deleting a customer')
    try:
        customer_delete = Customer.get(Customer.customer_id == customer_id)
        customer_delete.delete_instance()
        logger.info(f'Customer with ID {customer_id} deleted')

    except Exception as error:
        logger.info(f'Customer with ID {customer_id} not deleted')


def update_customer_credit(customer_id, credit_limit):
    """
    This method updates the customers credit
    """
    update_credit = Customer.update(credit_limit=credit_limit).where(
        Customer.customer_id == customer_id)
    logger.info(
        f'Raised credit limit to {credit_limit} for ID = {customer_id}')
    if not update_credit.execute():
        raise ValueError("NoCustomer")


def list_active_customers():
    '''
    This function counts the number of active customers
    '''
    try:
        logger.info('Counting active customers')
        query = (Customer.select(Customer.customer_id, Customer.status)
                 .where(Customer.status == 'active'))
        count = query.select().count()
    except Exception as error:
        logger.info('Customer does not exist')
    print(count)
    return count
