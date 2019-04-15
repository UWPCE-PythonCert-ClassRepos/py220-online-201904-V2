"""
    Basic operations for HP Norton database
"""


import logging
import src.db_model as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy import MetaData
# from sqlalchemy import Select

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("HP Norton Database")

engine = create_engine('sqlite:///HPNorton.db')
db_session = sessionmaker(bind=engine)
session = db_session()
metadata = MetaData(bind=engine)
customers = Table('Customer', metadata, autoload=True)
# table = meta.tables['customers']


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
        session.add(new_customer)
        session.commit()
        LOGGER.info("Adding record for %s", customer_id)
    except Exception as ex:
        LOGGER.info(ex)


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
    
    select_st = customers.select().where(customers.c.customer_id == customer_id)
    query = session.execute(select_st)
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
