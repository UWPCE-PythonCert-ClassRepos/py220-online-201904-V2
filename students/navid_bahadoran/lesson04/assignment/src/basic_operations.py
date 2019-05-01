# pylint: disable=W0401, R0903, C0103, W1203, W0614, E0602, E0401, R0913, E1111
"""Basic operation for our database"""

import logging
from peewee import *
from .model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, name, last_name, home_address, phone_number, email_address,
                 status, credit_limit):
    """ add_customer(customer_id, name, last name, home_address, phone_number,
    email_address, status, credit_limit): This function will add a new customer
    to the sqlite3 database."""
    try:
        with DB.transaction():
            Customer.create(
                customer_id=customer_id,
                name=name,
                last_name=last_name,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status.lower(),
                credit_limit=credit_limit,
            ).save()
            LOGGER.info("Adding record for %s", customer_id)
    except IntegrityError as ex:
        LOGGER.info(ex)
        raise IntegrityError("DoubleEntry")


def search_customer(customer_id):
    """search_customer(customer_id): This function will return a dictionary object with name,
    last_name, email address and phone number of a customer or an empty dictionary object if
    no customer was found."""
    query = Customer.select().where(Customer.customer_id == customer_id)
    find_customer = {}
    for customer in query:
        find_customer['customer_id'] = customer.customer_id
        find_customer['name'] = customer.name
        find_customer['last_name'] = customer.last_name
        find_customer['home_address'] = customer.home_address
        find_customer['phone_number'] = customer.phone_number
        find_customer['email_address'] = customer.email_address
        find_customer['status'] = customer.status
        find_customer['credit_limit'] = customer.credit_limit
    return find_customer


def delete_customer(customer_id):
    """ delete_customer(customer_id): This function will delete a customer from
    the sqlite3 database."""
    delete_item = Customer.delete().where(Customer.customer_id == customer_id)
    return bool(delete_item.execute())


def update_customer_credit(customer_id, credit_limit):
    """update_customer_credit(customer_id, credit_limit): This function will search
    an existing customer by customer_id and update their credit limit or raise a
    ValueError exception if the customer does not exist."""
    update_item = Customer.update(credit_limit=credit_limit).where(
        Customer.customer_id == customer_id).execute()
    if not update_item:
        raise ValueError("NoCustomer")
    else:
        return update_item


def list_active_customers():
    """list_active_customers(): This function will
    return an integer with the number of customers whose status is currently active."""
    return Customer.select().where(fn.LOWER(Customer.status) == "active").count()


DB.close()
