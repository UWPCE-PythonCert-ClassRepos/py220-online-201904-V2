import logging
from peewee import *
import db_models 



logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("customer database")


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
    """Adds a new customer to the customer database
    Raises IntegrityError from trying to insert a
    duplicate primary key.
    """
    try:
        with db_models.database.transaction():
            db_models.Customer.create(
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
    except IntegrityError as e:
        LOGGER.info(e)
        raise IntegrityError



def search_customer(customer_id):
    """Search for a specified customer."""

    query = db_models.Customer.select(db_models.Customer).where(
        db_models.Customer.customer_id == customer_id
    )
    cust = {}
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
    """Deletes the a customer from the database."""

    query = db_models.Customer.delete().where(db_models.Customer.customer_id == customer_id)
    return bool(query.execute())


def update_customer_credit(customer_id, credit_limit):
    """Updates the customer's credit limit."""

    query = db_models.Customer.update(credit_limit=credit_limit).where(
        db_models.Customer.customer_id == customer_id
    )
    if not query.execute():
        raise ValueError("NoCustomer")
    return True


def list_active_customers():
    """Specifies the number of active customers."""

    return (
        db_models.Customer.select()
        .where(fn.LOWER(db_models.Customer.status == "active"))
        .count()
    )

