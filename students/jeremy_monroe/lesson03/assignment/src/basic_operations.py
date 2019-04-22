""" The basic functions to handle interactions with customer records. """
from customer_models import Customer, CustomerCredit, CustomerStatus
from customer_models import DB, LOGGER


def add_customer(new_id, new_name, new_lastname, new_home_address,
                 new_phone_number, new_email_address, new_status,
                 new_credit_limit):
    """ The function to add a new customer. """
    try:
        with DB.transaction():
            LOGGER.info("Attempting to add customer")
            new_cust = Customer.create(
                customer_id=new_id,
                name=new_name,
                lastname=new_lastname,
                home_address=new_home_address,
                phone_number=new_phone_number,
                email_address=new_email_address
            )

            new_cust.save()

            LOGGER.info("Attempting to add customer credit limit")
            new_credit_limit = CustomerCredit.create(
                customer=new_cust,
                credit_limit=new_credit_limit)
            new_credit_limit.save()

            LOGGER.info("Attempting to add customer status")
            new_status = CustomerStatus.create(
                customer=new_cust, status=new_status)
            new_status.save()

    except Exception as exception:
        LOGGER.info("Error adding new customer.")
        LOGGER.info("Customer id = %s", new_id)
        LOGGER.info(exception)
    else:
        LOGGER.info("Customer added successfully!")

    DB.close()


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

        credit_limit_to_delete = CustomerCredit.get(
            CustomerCredit.customer == cust_to_delete)
        credit_limit_to_delete.delete_instance()

        status_to_delete = CustomerStatus.get(
            CustomerStatus.customer == cust_to_delete)
        status_to_delete.delete_instance()

        cust_to_delete.delete_instance()
    except Exception as exception:
        LOGGER.info("Unable to delete customer.")
        LOGGER.info(exception)
        return False
    else:
        LOGGER.info("Customer successfully deleted")

    DB.close()
    return True


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
