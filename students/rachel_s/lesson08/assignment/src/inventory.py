#!/usr/bin/env python3

'''
Lesson 08

Functions to add furniture to a CSV file.
'''

import csv
from pathlib import Path
from functools import partial

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
        open_type = 'a'
    else:
        open_type = 'w'
    with open(my_inv, open_type) as my_file:
        my_file.write(','.join([
            customer_name,
            item_code,
            item_description,
            str(item_monthly_price)
            ]))
        my_file.write('\n')


def single_customer(customer_name, invoice_file):
    '''
    Returns a function that takes one parameter: rental_items. This
    function iterates through rental_items and adds each item to
    invoice_file.
    '''
    # Create function with pre-assigned invoice file and customer name
    add_item = partial(
        add_furniture,
        invoice_file=invoice_file,
        customer_name=customer_name
    )

    # Create function for output
    def invoicer(rental_items):
        # Get data from rental_items file
        # ps DictReader is the greatest
        inv_data = []
        with open(rental_items, 'r') as file:
            reader = csv.DictReader(file, fieldnames=[
                'item_code',
                'item_description',
                'item_monthly_price'
            ])
            for row in reader:
                inv_data.append(dict(row))
        # Apply add_item function to each row from rental_items
        for line in inv_data:
            add_item(
                item_code=line['item_code'],
                item_description=line['item_description'],
                item_monthly_price=line['item_monthly_price']
            )
    return invoicer
