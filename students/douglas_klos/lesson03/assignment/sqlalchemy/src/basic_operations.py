#pylint: disable=E0401
"""
    Basic operations for HP Norton database
"""


import logging
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import func
from sqlalchemy import exc
import src.db_model as db

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("HP Norton Database")

ENGINE = create_engine("sqlite:///HPNorton.db")
DB_SESSION = sessionmaker(bind=ENGINE)
SESSION = DB_SESSION()
METADATA = MetaData(bind=ENGINE)
CUSTOMERS = Table("Customer", METADATA, autoload=True)


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
        new_customer = db.Customer(
            customer_id=customer_id,
            name=name,
            last_name=lastname,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            status=status.lower(),
            credit_limit=credit_limit,
        )
        SESSION.add(new_customer)
        SESSION.commit()
        LOGGER.info("Adding record for %s", customer_id)
    except sqlite3.IntegrityError as ex:
        LOGGER.info(ex)
        raise exc.IntegrityError


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
    select_st = CUSTOMERS.select().where(CUSTOMERS.c.customer_id == customer_id)
    query = SESSION.execute(select_st)
    for item in query:
        cust["customer_id"] = item.customer_id
        cust["name"] = item.name
        cust["lastname"] = item.last_name
        cust["email"] = item.email_address
        cust["phone_number"] = item.phone_number
        cust["home_address"] = item.home_address
        cust["status"] = item.status
        cust["credit_limit"] = item.credit_limit

    return cust


def delete_customer(customer_id):
    """Deletes the specified customer from database.

    Arguments:
        customer_id {string} -- Unique identifier for customer.

    Returns:
        bool -- Ture if successful, False if not.
    """
    if search_customer(customer_id) == {}:
        return False
    query = CUSTOMERS.delete().where(CUSTOMERS.c.customer_id == customer_id)
    query.execute()
    if search_customer(customer_id) == {}:
        return True
    raise Exception("Deletion failed")


def list_active_customers():
    """Returns an integer specifying the number of active customers

    Returns:
        integer -- Number of active customers
    """

    return (
        SESSION.query(CUSTOMERS)
        .filter(CUSTOMERS.c.status == "active")
        .statement.with_only_columns([func.count()])
        .scalar()
    )


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
    if search_customer(customer_id) == {}:
        raise ValueError

    SESSION.query(db.Customer).filter(
        db.Customer.customer_id == customer_id
    ).update({"credit_limit": credit_limit})
    return SESSION.commit()
