# pylint: disable=E0401, R0913, W0401, E0602, W0703
"""
    Basic operations for HP Norton database
"""


import logging
from peewee import *
import src.db_model as db


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("HP Norton Database")


def add_customer(
        customer_id,
        name,
        lastname,
        home_address,
        phone_number,
        email_address,
        status,
        credit_limit,
):
    """Adds a new customer to the HPNorton database

    Arguments:
        customer_id {string} -- Unique identifier for customer
        name {string} -- First name of customer
        lastname {string} -- Last name of customer
        home_address {string} -- Home address of customer
        phone_number {string} -- Phone number of customer
        email_address {string} -- Email address of customer
        status {string} -- Active / Inactive status of customer
        credit_limit {int} -- Credit limit of customer

    Raises:
        IntegrityError -- Raised when trying to insert a duplicate primary key.
    """
    try:
        with db.database.transaction():
            db.Customer.create(
                customer_id=customer_id,
                name=name,
                last_name=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status.lower(),
                credit_limit=credit_limit,
            )
            LOGGER.info("Adding record for %s", customer_id)
    except IntegrityError as ex:
        LOGGER.info(ex)
        raise IntegrityError


def search_customer(customer_id):
    """Search for specified customer and returns their data.

    Arguments:
        customer_id {string} -- Unique identifier for customer.

    Returns:
        dictionary -- Object containing name, lase_name, email, phone_number
                            for specified customer_id.  Returns empty dict
                            if customer not found.
    """
    cust = {}

    try:
        item = db.Customer.get(db.Customer.customer_id == customer_id)
        cust["customer_id"] = item.customer_id
        cust["name"] = item.name
        cust["lastname"] = item.last_name
        cust["email"] = item.email_address
        cust["phone_number"] = item.phone_number
        cust["home_address"] = item.home_address
        cust["status"] = item.status
        cust["credit_limit"] = item.credit_limit
        return cust
    # This is what is thrown, but when I try to catch it comes back not defined.
    # except CustomerDoesNotExist as ex:
    except Exception: # as ex:
        # print(f"{type(ex).__name__}")
        return cust


def delete_customer(customer_id):
    """Deletes the specified customer from database.

    Arguments:
        customer_id {string} -- Unique identifier for customer.

    Returns:
        bool -- Ture if successful, False if not.
    """
    query = db.Customer.delete().where(db.Customer.customer_id == customer_id)
    return bool(query.execute())


def update_customer_credit(customer_id, credit_limit):
    """Update the credit limit of the specified customer.

    Arguments:
        customer_id {string} -- Unique identifier for customer
        credit_limit {float} -- New credit limit for customer

    Raises:
        ValueError -- Raises ValueError if customer_id not in database.

    Returns:
        bool -- Ture if successful, False if not.
    """
    query = db.Customer.update(credit_limit=credit_limit).where(
        db.Customer.customer_id == customer_id
    )
    if not query.execute():
        raise ValueError("NoCustomer")
    return True


def list_active_customers():
    """Returns an integer specifying the number of active customers

    Returns:
        integer -- Number of active customers
    """
    return (
        db.Customer.select()
        .where(fn.LOWER(db.Customer.status == "active"))
        .count()
    )
