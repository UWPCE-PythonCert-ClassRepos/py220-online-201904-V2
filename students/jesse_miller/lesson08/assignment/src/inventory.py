#!/usr/bin/env python3
'''
Inventory management through functional programming
'''
import csv
from pathlib import Path
from functools import partial

def add_furniture(invoice_file='', customer_name='', item_code='',
                  item_description='', item_monthly_price=''):
    '''
    Updates the master invoice file which lists which furniture is rented to
    which customer. It create a new file if one doesn't already exist.
    '''


    with open(invoice_file, 'a+', newline='') as csvfile:
        '''
        This will be the write to the csv.  Surprised, right?
        '''
        writer = csv.writer(csvfile)
        row = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(row)

def add_test_data():
    '''
    Populating the test date into the file.
    '''
    add_furniture('invoice_file.csv', 'Elisa Miles', 'LR04', 'Leather Sofa',
                  '25.00')
    add_furniture('invoice_file.csv', 'Edward Data', 'KT78', 'Kitchen Table',
                  '10.00')
    add_furniture('invoice_file.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress',
                  '17.00')
