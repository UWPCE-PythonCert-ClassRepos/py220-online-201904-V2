#!/usr/bin/env python3
# pylint: disable=W0106
""" HPNorton - Lesson 08 - Currying and Closures """

from csv import writer, reader
from functools import partial


def add_furniture(invoice_file, customer_name,
                  item_code, item_description, item_monthly_rate):
    """ Add a new piece of furniture to invoice_file

    Arguments:
        invoice_file {string} -- Name of invoice file to write to
        customer_name {string} -- Customer Name
        item_code {string} -- Item Code
        item_description {string} -- Description of item
        item_monthly_rate {float} -- Monthly rate for item
    """

    with open(invoice_file, "a") as csv_file:
        writer(csv_file).writerow(
            [customer_name, item_code, item_description, item_monthly_rate]
        )


def single_customer(customer_name, invoice_file):
    """ Closure for inserting into add_furniture

    Arguments:
        customer_name {string} -- Name of csutomer to insert
        invoice_file {string} -- Invoice file to insert into

    Returns:
        function(rental_file) -- Closed function for inserting rentals
    """

    def function(rental_file):
        """ Adds to invoice file rentals from rental_file

        Closure:
            customer_name {string} -- Name of customer to insert
            invoice_file {string} -- Invoice file to insert into

        Arguments:
            rental_file {string} -- File containing new rentals for customer
        """

        add_furn = partial(add_furniture, invoice_file, customer_name)
        with open(rental_file, "r") as csv_file:
            [add_furn(*x) for x in reader(csv_file)]

    return function


def single_customer_search(customer_name, invoice_file):
    """ Closure for searching for customers rentals

    Arguments:
        customer_name {string} -- Name of csutomer to insert
        invoice_file {string} -- Invoice file to insert into

    Returns:
        function(rental_file) -- Closed function that returns rentals
    """

    def function(rental_items):
        """[summary]

        Arguments:
            rental_items {string} -- Rental item to search for

        Closure:
            customer_name {string} -- Name of customer to insert
            invoice_file {string} -- Invoice file to insert into
        """

        with open(invoice_file, "r") as csv_file:
            rental_list = [
                line
                for line in list(reader(csv_file))
                if line != [] and line[0] == customer_name and line[1] == rental_items
            ]
        if not rental_list:
            return "Nothing Found"
        return rental_list

    return function
