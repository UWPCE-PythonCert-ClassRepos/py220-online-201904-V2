#!/usr/bin/env python3

'''
Lesson 08

Functions to add furniture to a CSV file.
'''

# Rachel Schirra
# May 27, 2019
# Python 220 Lesson 08


'''
Create a function called add_furniture that takes the following input
parameters:

invoice_file
customer_name
item_code
item_description
item_monthly_price

This function will create invoice_file (to replace the spreadsheet’s
data) if it doesn’t exist or append a new line to it if it does. After
adding a few items to the same file, the file created by add_furniture
should look something like this:

Elisa Miles,LR04,Leather Sofa,25.00
Edward Data,KT78,Kitchen Table,10.00
Alex Gonzales,BR02,Queen Mattress,17.00

You can create a starter file in this format for testing, or you can
have your add function do it.
'''

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
    pass


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

