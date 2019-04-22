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


def add_customer(customer_id,
                 name,
                 lastname,
                 home_address,
                 phone_number,
                 email,
                 status,
                 credit_limit):
    """
    Function to add customers to the customer table.
    :param args: an iterable of customer information
    :return: customer table is populated
    """
    # pylint: disable = W0703
    try:
        with DB.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email=email,
                status=status.lower(),
                credit_limit=credit_limit)
            new_customer.save()
        logging.info('Customer(s) successfully added')

    except Exception as error:
        LOGGER.info(f'Error creating = {name}')
        LOGGER.info(error)


def search_customer(cust_id):
    """
    returns values of selected user
    :param cust_id:
    :return: name, lastname, email, phone number
    """
    query = (Customer
             .select(Customer.customer_id, Customer.name, Customer.lastname,
                     Customer.email, Customer.phone_number,
                     Customer.home_address, Customer.status,
                     Customer.credit_limit)
             .where(Customer.customer_id == cust_id))
    result = {}
    for person in query:
        result["customer_id"] = person.customer_id
        result["name"] = person.name
        result["lastname"] = person.lastname
        result["email"] = person.email
        result["phone_number"] = person.phone_number
        result["home_address"] = person.home_address
        result["status"] = person.status
        result["credit_limit"] = person.credit_limit
    return result


def delete_customer(customer_id):
    """
    Deletes a customer specified by customer id
    :param cust_id:
    :return: record is deleted
    """
    del_query = Customer.get(Customer.customer_id == customer_id)
    return bool(del_query.delete_instance())


def update_customer_credit(cust_id, credit_limit):
    """
    Query that updates a specific customer's credit limit.
    :param cust_id:
    :param new_credit_limit:
    :return: Updated credit limit
    """
    update_query = Customer.update(credit_limit=credit_limit) \
        .where(Customer.customer_id == cust_id)
    if not update_query.execute():
        raise ValueError("Record does not exist")
    return True


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
        return count.cust_count


def del_all_records():
    """
    Deletes all records. Used only for testing purposes.
    :return: An empty customer table
    """
    delete_alles = Customer.delete().where(Customer.name >= '')
    delete_alles.execute()


if __name__ == '__main__':
    # add_customer(CUSTOMERS)
    # print((123))
    # del_customers(123)
    # print(search_customers(123))
    # update_customer_credit(456, 10000)
    # update_customer_credit(654, 10000)
    print(search_customer(997))
    # print(list_active_customers())
    # del_all_records()
    print(list_active_customers())

    DB.close()
