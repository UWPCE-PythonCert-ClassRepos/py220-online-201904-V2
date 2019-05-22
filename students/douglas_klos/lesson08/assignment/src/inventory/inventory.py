#!/usr/bin/env python3

""" HPNorton - Lesson 08 - Currying and Closures """

from os.path import isfile
from csv import writer, reader
from functools import partial, reduce


def add_furniture(
    invoice_file, customer_name, item_code, item_description, item_monthly_rate
):
    """ Add new furniture to the invoice_file """

    new_item = [customer_name, item_code, item_description, item_monthly_rate]

    if isfile(invoice_file):
        with open(invoice_file, "a") as csv_file:
            writer(csv_file).writerow(new_item)
    else:
        with open(invoice_file, "r") as csv_file:
            writer(csv_file).writerow(new_item)


def single_customer(customer_name, invoice_file):
    """ Closure """
    def function(rental_file):
        add_furn = partial(add_furniture, invoice_file, customer_name)
        with open(rental_file, "r") as csv_file:
            [add_furn(*x) for x in reader(csv_file)]

    return function


def single_customer_search(customer_name, invoice_file):
    def function(rental_items):
        rental_list = []
        with open(invoice_file, "r") as csv_file:
            rental_list = [
                line
                for line in list(reader(csv_file))
                if line[0] == customer_name and line[1] == rental_items
            ]
        if len(rental_list) == 0:
            return "Nothing Found"
        return rental_list

    return function
