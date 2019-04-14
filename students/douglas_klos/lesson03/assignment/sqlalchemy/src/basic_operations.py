#!/usr/bin/env python3
"""
    Basic operations for HP Norton database
"""


import logging
from db_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("HP Norton Database")


class HPNorton():
    def __init__(self):
        pass

    def add_customer(customer_id, name, lastname, home_address,
                     phone_number, email_address, status, credit_limit):
        """Adds a new customer to the HPNorton database

        Arguments:
            customer_id {string} -- Unique identifier for customer
            name {string} -- First name of customer
            lastname {string} -- Last name of customer
            home_address {string} -- Home address of customer
            phone_number {string} -- Phone number of customer
            email_address {string} -- Email address of customer
            status {string} -- Active / Inactive status of customer
            credit_limit {float} -- Credit limit of customer
        """

        pass

    def search_customer(customer_id):
        """Search for specified customer and returns their data.

        Arguments:
            customer_id {string} -- Unique identifier for customer.

        Returns:
            dictionary -- Object containing name, lase_name, email, phone_number
                              for specified customer_id.  Returns empty dict
                              if customer not found.
        """
        return {}

    def delete_customer(customer_id):
        """Deletes the specified customer from database.

        Arguments:
            customer_id {string} -- Unique identifier for customer.

        Returns:
            bool -- Ture if successful, False if not.
        """
        return True

    def update_customer(customer_id, credit_limit):
        """Update the credit limit of the specified customer.

        Arguments:
            customer_id {string} -- Unique identifier for customer
            credit_limit {float} -- New credit limit for customer

        Raises:
            ValueError -- Raises ValueError if customer_id not in database.

        Returns:
            bool -- Ture if successful, False if not.
        """
        return True

    def list_active_customers():
        """Returns an integer specifying the number of active customers

        Returns:
            integer -- Number of active customers
        """
        return 100
