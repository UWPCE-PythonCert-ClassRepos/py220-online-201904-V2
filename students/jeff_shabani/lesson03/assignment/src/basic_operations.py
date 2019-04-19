"""
module for basic customer database operations including:
adding, searching, deleting, updating, and listing customers.
"""
import logging

from peewee import *
from customer_model import Customer


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DB = SqliteDatabase('customers.db')
DB.connect()

CUSTOMER_ID = 0
NAME = 1
LASTNAME = 2
ADDRESS = 3
PHONE_NUMBER = 4
EMAIL = 5
STATUS = 6
CREDIT_LIMIT = 7

CUSTOMERS = [
    ("123", "Jurgen", "Muller", "337 Eichmann Locks", "1-615-598-8649 x975",
     "Jurgen@muller.net", "Active", 237),
    ("456", "Jens", "Blau", "765 Holstein Dr", "206.765.9087", "jb@mail.com",
     "active", 0),
    ("345", "Sven", "Kruse", "421 W. Galer", "206-908-2194", "svenk@wetten.de",
     "active", -10),
    ("0123", "Thor", "Weiss", "908 Howe St", "780-965-1243",
     "niemann@nichts.com", "active", 999),
    ("777", "Oskar", "Kratz", "67 Harald Dr", "905.987.3421",
     "ingen@vivs.no", "active", 999)
]


def _add_customers(*args):
    """
    Function to add customers to the customer table.
    :param args: an iterable of customer information
    :return: customer table is populated
    """
    # pylint: disable = W0703
    for record in args:
        for customer in record:
            try:
                with DB.transaction():
                    new_customer = Customer.create(
                        customerid=customer[CUSTOMER_ID],
                        name=customer[NAME],
                        lastname=customer[LASTNAME],
                        home_address=customer[ADDRESS],
                        phone_number=customer[PHONE_NUMBER],
                        email=customer[EMAIL],
                        status=customer[STATUS],
                        credit_limit=customer[CREDIT_LIMIT])
                    new_customer.save()
                logging.info('Customer(s) successfully added')

            except Exception as error:
                LOGGER.info(f'Error creating = {customer[NAME]}')
                LOGGER.info(error)


def _search_customers(cust_id):
    """
    returns values of selected user
    :param cust_id:
    :return: name, lastname, email, phone number
    """
    query = (Customer
             .select(Customer.name, Customer.lastname, Customer.email,
                     Customer.phone_number, Customer.credit_limit)
             .where(Customer.customerid == cust_id))

    if [e.values() for e in query.dicts()] == []:
        return dict()

    return f'{[e.values() for e in query.dicts()]}'


def _del_customers(cust_id):
    """
    Deletes a customer specified by customer id
    :param cust_id:
    :return: record is deleted
    """
    del_query = Customer.get(Customer.customerid == cust_id)
    del_query.delete_instance()


def _update_customer_credit(cust_id, new_credit_limit):
    """
    Query that updates a specific customer's credit limit.
    :param cust_id:
    :param new_credit_limit:
    :return: Updated credit limit
    """
    try:
        update_query = Customer.update(credit_limit=new_credit_limit) \
            .where(Customer.customerid == cust_id)
        update_query.execute()
    except ValueError:
        print(f'Record record doe not exist')


def _list_active_customers():
    """
    Returns number of active customers.
    :return: integer representing count
    """
    count_query = (Customer
                   .select(Customer, fn.COUNT(Customer.name)
                           .alias('cust_count'))
                   .where(Customer.status == str.lower('Active')))
    for count in count_query:
        return f'There are {count.cust_count} active customers'


def _del_all_records():
    """
    Deletes all records. Used only for testing purposes.
    :return: An empty customer table
    """
    delete_alles = Customer.delete().where(Customer.name >= '')
    delete_alles.execute()


if __name__ == '__main__':
    # _add_customers(CUSTOMERS)
    # print(_search_customers(123))
    # _del_customers(123)
    # print(_search_customers(123))
    # _update_customer_credit(456, 10000)
    # _update_customer_credit(654, 10000)
    # print(_search_customers(456))
    # print(_list_active_customers())
    # _del_all_records()
    # print(_list_active_customers())

    DB.close()
