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
        ("123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("456", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("789", "Name", "Lastname", "Address", "phone", "email", "active", 0),
        ("345", "Name", "Lastname", "Address", "phone", "email", "active", -10),
        ("0123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("777", "Name", "Lastname", "Address", "phone", "email", "active", 999)
    ]


def add_customer(*args):
    """
    Function to add customers to the customer table.
    :param args: an iterable of customer information
    :return: customer table is populated
    """
    # pylint: disable = W0703
    # unpack the args tuple
    customer, *empty_list = args
    for num in range(len(customer)):
        try:
            with DB.transaction():
                new_customer = Customer.create(
                    customer_id=customer[num][CUSTOMER_ID],
                    name=customer[num][NAME],
                    lastname=customer[num][LASTNAME],
                    home_address=customer[num][ADDRESS],
                    phone_number=customer[num][PHONE_NUMBER],
                    email=customer[num][EMAIL],
                    status=str.lower(customer[num][STATUS]),
                    credit_limit=int(customer[num][CREDIT_LIMIT]))
                new_customer.save()
            logging.info('Customer(s) successfully added')

        except Exception as error:
            LOGGER.info(f'Error creating = {customer[NAME]}')
            LOGGER.info(error)


def search_customers(cust_id):
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


def del_customers(cust_id):
    """
    Deletes a customer specified by customer id
    :param cust_id:
    :return: record is deleted
    """
    del_query = Customer.get(Customer.customerid == cust_id)
    del_query.delete_instance()


def update_customer_credit(cust_id, new_credit_limit):
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


def list_active_customers():
    """
    Returns number of active customers.
    :return: integer representing count
    """
    count_query = (Customer
                   .select(Customer, fn.COUNT(Customer.name)
                           .alias('cust_count'))
                   .where(Customer.status == 'active'))
    for count in count_query:
        return f'There are {count.cust_count} active customers'


def del_all_records():
    """
    Deletes all records. Used only for testing purposes.
    :return: An empty customer table
    """
    delete_alles = Customer.delete().where(Customer.name >= '')
    delete_alles.execute()


if __name__ == '__main__':
    add_customer(CUSTOMERS)
    # print((123))
    # del_customers(123)
    # print(search_customers(123))
    # update_customer_credit(456, 10000)
    # update_customer_credit(654, 10000)
    # print(search_customers(456))
    # print(list_active_customers())
    # del_all_records()
    print(list_active_customers())

    DB.close()
