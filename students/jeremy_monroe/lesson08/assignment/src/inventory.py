"""
Jeremy Monroe Assignment 08

I left the 'if __name__' block empty. Instead, running test_assignment_08 via
pytest will utilize each of my functions in turn and make use of functools
partial.
"""

import os
import csv


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """
    Creates or adds to an invoice file populating or updating it with the
    data from the provided parameters.
    """
    if os.path.isfile(invoice_file):
        with open(invoice_file, 'a', newline='') as write_file:
            # print(write_file)
            writer = csv.writer(write_file)
            writer.writerow([customer_name, item_code, item_description,
                             item_monthly_price])
    else:
        with open(invoice_file, "w+", newline='') as write_file:
            writer = csv.writer(write_file)
            writer.writerow([customer_name, item_code, item_description,
                             item_monthly_price])


def single_customer(customer_name, invoice_file):
    """
    Returns a function that that takes the parameter rental_items.
    """
    def single_customer_inner(rental_items):
        """
        When called will use the previously specified parameters in conjunction
        with rental_items to save all relevant data to a csv file utilizing
        add_furniture.
        """
        with open(rental_items, 'r') as read_file:
            for line in csv.reader(read_file, delimiter=','):
                add_furniture(invoice_file, customer_name,
                              line[0], line[1], line[2])
    return single_customer_inner


def single_customer_partial(customer_name, invoice_file, rental_items):
    """
    Could be called as is passing in all necessary parameters.
    The intention is to use this in conjunction with partial allowing for easy
    creation of multiple new records for the same customer.
    """
    with open(rental_items, 'r') as read_file:
        for line in csv.reader(read_file, delimiter=','):
            add_furniture(invoice_file, customer_name,
                          line[0], line[1], line[2])


if __name__ == "__main__":
    pass
