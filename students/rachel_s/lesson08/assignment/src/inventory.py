#!/usr/bin/env python3

'''
Lesson 08

Functions to add furniture to a CSV file.
'''

from pathlib import Path

# Rachel Schirra
# May 27, 2019
# Python 220 Lesson 08


def add_furniture(
        invoice_file,
        customer_name,
        item_code,
        item_description,
        item_monthly_price
    ):
    '''
    Adds an item to the file invoice_file. If the file specified does
    not exist, it creates the file and then adds the item.
    '''
    my_inv = Path(invoice_file)
    if my_inv.is_file():
        my_file = open(my_inv, 'a')
    else:
        my_file = open(my_inv, 'w')
    my_file.write(','.join([
        customer_name,
        item_code,
        item_description,
        item_monthly_price
        ]))
    my_file.close()


'''
Create a function called single_customer:

Input parameters: customer_name, invoice_file.

Output: Returns a function that takes one parameter, rental_items.

single_customer needs to use functools.partial and closures, in order
to return a function that will iterate through rental_items and add each
item to invoice_file.
'''

def single_customer(customer_name, invoice_file):
    '''
    Returns a function that takes one parameter: rental_items. This
    function iterates through rental_items and adds each item to
    invoice_file.
    '''
