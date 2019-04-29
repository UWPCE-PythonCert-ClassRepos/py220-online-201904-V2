""" The basic functions to handle interactions with customer records. """
import csv
from customer_models import Customer, CustomerCredit, CustomerStatus
from customer_models import DB, LOGGER


def add_customer(new_id, new_name, new_lastname, new_home_address,
                 new_phone_number, new_email_address, new_status,
                 new_credit_limit):
    """
    The function to add a new customer.

    For my refactor I broke add_customer up into a few 'save' functions so that
    data for each of my database tables is saved to the database by I separate
    function.
    """
    new_cust = save_customer(new_id, new_name, new_lastname,
                             new_home_address, new_phone_number, new_email_address)
    save_credit_limit(new_cust, new_credit_limit)
    save_customer_status(new_cust, new_status)

    DB.close()


def save_customer(new_id, new_name, new_lastname, new_home_address,
                  new_phone_number, new_email_address):
    """ Saves a new customer to the database. """
    try:
        with DB.transaction():
            LOGGER.info("Attempting to save customer")
            new_cust = Customer.create(
                customer_id=new_id,
                name=new_name,
                lastname=new_lastname,
                home_address=new_home_address,
                phone_number=new_phone_number,
                email_address=new_email_address
            )

            new_cust.save()
    except Exception as exception:
        LOGGER.info("Error saving new customer.")
        LOGGER.info("Customer id = %s", new_id)
        LOGGER.info(exception)

        # I've included this return so that the other two save functions will
        # work without a big nasty error if a customer already exists.
        return Customer.get(Customer.customer_id == new_id)
    else:
        LOGGER.info("Customer saved successfully!")
        return new_cust


def save_credit_limit(new_cust, new_credit_limit):
    """ Saves a new customer credit limit to the database. """
    try:
        with DB.transaction():
            LOGGER.info("Attempting to add customer credit limit")
            new_credit_limit = CustomerCredit.create(
                customer=new_cust,
                credit_limit=new_credit_limit)
            new_credit_limit.save()
    except Exception as exception:
        LOGGER.info("Error saving new credit limit")
        LOGGER.info("Customer id = %s", new_cust.customer_id)
        LOGGER.info(exception)
    else:
        LOGGER.info("New credit limit saved successfully.")


def save_customer_status(new_cust, new_status):
    """ Saves a new customer status. """
    try:
        with DB.transaction():
            LOGGER.info("Attempting to add customer status")
            new_status = CustomerStatus.create(
                customer=new_cust, status=new_status)
            new_status.save()

    except Exception as exception:
        LOGGER.info("Error saving customer status.")
        LOGGER.info("Customer id = %s", new_cust.customer_id)
        LOGGER.info(exception)
    else:
        LOGGER.info("Customer status successfully!")


def search_customer(input_customer_id):
    """ The function to search for an individual customer. """
    try:
        LOGGER.info("Trying to find customer: %s", input_customer_id)
        customer = Customer.get(Customer.customer_id == input_customer_id)
    except Exception:
        LOGGER.info("Customer couldn't be found.")
        return {}

    LOGGER.info("Customer found, returning relevant info.")
    customer_dict = {'name': customer.name, 'lastname': customer.lastname,
                     'email': customer.email_address,
                     'phone_number': customer.phone_number}

    DB.close()
    return customer_dict


def delete_customer(input_customer_id):
    """ The function to delete an individual customer. """
    try:
        LOGGER.info("Trying to delete customer: %s", input_customer_id)

        cust_to_delete = Customer.get(
            Customer.customer_id == input_customer_id)

        delete_customer_status(cust_to_delete)
        delete_customer_credit_limit(cust_to_delete)

        cust_to_delete.delete_instance()
    except Exception as exception:
        LOGGER.info("Unable to delete customer.")
        LOGGER.info(exception)
        return False

    DB.close()
    return True


def delete_customer_status(cust_to_delete):
    """ Deletes a customer's status. """
    try:
        LOGGER.info("Trying to delete status for customer: %s",
                    cust_to_delete.customer_id)

        status_to_delete = CustomerStatus.get(
            CustomerStatus.customer == cust_to_delete)
        status_to_delete.delete_instance()

        cust_to_delete.delete_instance()
    except Exception as exception:
        LOGGER.info("Unable to delete customer status.")
        LOGGER.info(exception)
    else:
        LOGGER.info("Customer status deleted")


def delete_customer_credit_limit(cust_to_delete):
    """ Deletes a customer's credit limit. """
    try:
        LOGGER.info("Trying to delete credit limit for customer: %s",
                    cust_to_delete.customer_id)

        credit_limit_to_delete = CustomerCredit.get(
            CustomerCredit.customer == cust_to_delete)
        credit_limit_to_delete.delete_instance()

        cust_to_delete.delete_instance()
    except Exception as exception:
        LOGGER.info("Unable to delete customer credit limit.")
        LOGGER.info(exception)
    else:
        LOGGER.info("Customer credit limit deleted")


def update_customer_credit(input_customer_id, input_credit_limit):
    """ The function to update a customer's credit limit. """
    try:
        LOGGER.info(("Trying to update credit limit for customer:"
                     "%s"), input_customer_id)

        with DB.transaction():
            cust_to_update = CustomerCredit.select().join(Customer).where(
                Customer.customer_id == input_customer_id)
            cust_to_update[0].credit_limit = input_credit_limit
            cust_to_update[0].save()
    except Exception:
        LOGGER.info(
            "Error updating credit limit for customer %s", input_customer_id)
        LOGGER.info("Customer not found.")
        raise ValueError
    else:
        LOGGER.info("Successfully updated credit limit for customer: %s",
                    input_customer_id)

    DB.close()


def list_active_customers():
    """ The function to count the users whose status is set to 'active'. """
    LOGGER.info("Retrieving customers whose status is active")

    active_users = CustomerStatus.select().where(
        CustomerStatus.status == 'active').count()

    LOGGER.info("There are %s active users.", active_users)

    return active_users


if __name__ == '__main__':
    with open('../data/customer.csv') as infile:
        READ_CUSTOMERS = csv.reader(infile)

        #customer_list = [line for line in read_customers]

        CUSTOMER_GENERATOR = (line for line in READ_CUSTOMERS)
        next(CUSTOMER_GENERATOR)

        for i in range(10):
            cust_gen_current = next(CUSTOMER_GENERATOR)
            add_customer(cust_gen_current[0], cust_gen_current[1],
                         cust_gen_current[2], cust_gen_current[3],
                         cust_gen_current[4], cust_gen_current[5],
                         cust_gen_current[6], cust_gen_current[7])

        # for i in (line for line in READ_CUSTOMERS):
        #    add_customer(i[0], i[1],
        #            i[2], i[3],
        #            i[4], i[5],
        #            i[6], i[7])

    # for line in customer_list[:10]:
    #    add_customer(line[0], line[1], line[2], line[3], line[4], line[5],
    #            line[6], line[7])
