"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)

    Person:

        1. add a new record and delete it

"""
import logging
from customer_model import *


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    '''
    This function will add a new customer to the sqlite3 database.
    '''
    LOGGER.info('Add and display a Customer')
    with DATABASE.transaction():
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
        acustomer = Customer.get(Customer.customer_id == customer_id)
    LOGGER.info('Database %s add successful.', acustomer.customer_id)



def search_customer(customer_id):
    '''
    return a dictionary object with name, lastname, email address and
    phone number of a customer or an empty dictionary object if no
    customer was found
    '''
    LOGGER.info('Show customer')
    with DATABASE.transaction():
        try:
            acustomer = Customer.get(Customer.customer_id == customer_id)
            LOGGER.info('We found %s %s, %s, %s',
                        acustomer.customer_name, acustomer.customer_lastname,
                        acustomer.email_address, acustomer.phone_number)
        #if no customer was found
        # it was giving me model based error type 'CustomerDoesNotExist',
        # not sure what error type would work here?
        except Exception as error_message:
            LOGGER.info(error_message)
            return {}
    return {'name': acustomer.customer_name,
            'lastname': acustomer.customer_lastname,
            'email': acustomer.email_address,
            'phone_number': acustomer.phone_number}


def delete_customer(customer_id):
    '''
    This function will delete a customer from the sqlite3 database.
    '''
    LOGGER.info('Delete a customer')
    with DATABASE.transaction():
        try:
            acustomer = Customer.get(Customer.customer_id == customer_id)
            acustomer.delete_instance()
            LOGGER.info('Customer %s has been deleted.', customer_id)
        # it was giving me model based error type,
        # not sure what error type would work here?
        except Exception as error_message:
            LOGGER.info(error_message)


def update_customer_credit(customer_id, credit_limit):
    '''This function will search an existing customer by customer_id
    and update their credit limit or raise a ValueError exception if
    the customer does not exist.
    '''
    LOGGER.info('update a customer credit limit')
    with DATABASE.transaction():
        try:
            acustomer = Customer.get(Customer.customer_id == customer_id)
            acustomer.credit_limit = credit_limit
            acustomer.save()
            LOGGER.info("Customer %s's credit limit has been changed to %s.",
                        acustomer.customer_id, acustomer.credit_limit)
        except Exception as error_message:
            LOGGER.info(error_message)
            raise ValueError('NoCustomer')


def list_active_customers():
    '''This function will return an integer with the number of customers
    whose status is currently active.
    '''
    LOGGER.info('Return an integer with the number of customers who are active')
    with DATABASE.transaction():
        #query = Customer.select(Customer.customer_id,
                                # fn.COUNT(Customer.status == "Active"))
        #count = query.scalar()
        query = (Customer.select(Customer.customer_id, Customer.status)
                 .where(Customer.status == 'Active'))
        count = query.select().count()
        #for customer in query:
            #LOGGER.info('Customer ID is %s',customer.customer_id)
        return count


#test
if __name__ == '__main__':
#    add_customer('c11110', 'bill', 'smith', '11th st', '316-2342',
#                 'etet@gmil', 'Active', 100)
    print(search_customer('c11110'))
#    update_customer_credit('c11110', 200)
#    delete_customer('c11110')
#    print(list_active_customers())


DATABASE.close()
