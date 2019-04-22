"""
Program to manipulate customer database.

"""
# pylint: disable=W1203, R0913, W0703, C0303, C0121

import logging
import peewee 
#import src.db_model as db


from customer_model import Customer

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)

def add_customer(customer_id, name, lastname, home_address, phone_number,

                 email_address, status, credit_limit):

    """This function will add a new customer to the sqlite3 database."""

    LOGGER.info('Adding a new customer')

    try:
        new_customer = Customer.create(

            customer_id=customer_id,

            customer_name=name,

            customer_last_name=lastname,

            customer_address=home_address,

            customer_phone=phone_number,

            customer_email=email_address,

            customer_status=status,

            customer_limit=credit_limit)
        new_customer.save()
        LOGGER.info('Database add successful')
        LOGGER.info(f'Customer: {name} '
                    f'{lastname} saved as'
                    f' {customer_id}')

    except peewee.IntegrityError:
        LOGGER.info(f'{customer_id} already exists in database')
        raise ValueError('Customer already exists in the database') from None
    except Exception as err:
        LOGGER.info(f'Error creating = {customer_id} - check all inputs.')
        LOGGER.info(err)


def search_customer(customer_id):

    """
    This function will return a dictionary object with name, lastname,
    email address and phone number of a customer or an empty dictionary
    object if no customer was found.
    """
    LOGGER.info(f'Searching for a customer with customer id: {customer_id}')

    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)

        LOGGER.info(f'{acustomer.customer_id} found!')
        return {'name': acustomer.customer_name,
                'lastname': acustomer.customer_last_name,
                'email': acustomer.customer_email,
                'phone_number': acustomer.customer_phone}

    except Exception as err:
        LOGGER.info(err)
        LOGGER.info(f'{customer_id} not found in database. '
                    'Empty dict to be returned')
        return {}

def delete_customer(customer_id):
    """This function will delete a customer from the sqlite3 database."""
    LOGGER.info('Deleting a customer')
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info(f'Trying to delete {acustomer.customer_name}'
                    f' {acustomer.customer_last_name}')
        acustomer.delete_instance()
        LOGGER.info(f'{customer_id} successfully deleted from database')

    except Exception as err:
        LOGGER.info(f'{customer_id} not deleted!'
                    ' Customer ID not found in database')
        LOGGER.info(err)

        
def update_customer_credit(customer_id, credit_limit):
    """
    This function will search an existing customer by customer_id
    and update their credit limit or raise a ValueError exception if the
    customer does not exist.
    """
    LOGGER.info('Updating customer credit limit')
    try:
        LOGGER.info('Checking if inputted credit limit is float type')
        float(credit_limit)
        LOGGER.info(f'{credit_limit} is type float')
    except Exception as err:
        LOGGER.info(err)
        LOGGER.info(f'{credit_limit} not float type')
        raise TypeError(f'{credit_limit} NOT valid!') from None    
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info(f'{customer_id} found in database!')
        acustomer.customer_limit = credit_limit
        acustomer.save()
    except (IndexError, Exception) as err:
        LOGGER.info(f'Customer id {customer_id} not found in database')
        raise ValueError(f'{customer_id} NOT found in database!') from None

    
def list_active_customers():
    """
    This function will return an integer with the number of
    customers whose status is currently active.
    """
    LOGGER.info('Listing active customers')    
    query = Customer.select().where(Customer.customer_status == True).count()
    LOGGER.info(f'{query} customers are active')
    return query
