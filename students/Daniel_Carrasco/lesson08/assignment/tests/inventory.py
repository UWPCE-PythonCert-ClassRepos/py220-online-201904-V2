"""
Lesson 8 assignment
"""
# pylint: disable=E1121

import csv
from functools import partial

def add_furniture(
        invoice_file,
        customer_name,
        item_code,
        item_description,
        item_monthly_price):
    '''
    method to create an inventory file
    '''

    with open(invoice_file, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        data = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(data)
    return customer_name, item_code, item_description, item_monthly_price


def single_customer(invoice_file, customer_name):
    '''
    method that uses partial function to add a single customer
    '''
    add_single = partial(add_furniture, invoice_file, customer_name)

    def partial_function(rental_file):
        with open(rental_file, 'r') as file:
            reader = csv.reader(file)
            return_list = [add_single(*line) for line in reader]
        return return_list
    return partial_function

if __name__ == "__main__":
    add_furniture(
        "rented_items.csv",
        "Elisa Miles",
        "LR04",
        "Leather Sofa",
        25)
    add_furniture(
        "rented_items.csv",
        "Edward Data",
        "KT78",
        "Kitchen Table",
        10)
    add_furniture(
        "rented_items.csv",
        "Alex Gonzales",
        "ADM4",
        "Queen Mattress",
        17)
    CREATE_INVOICE = single_customer("rented_items.csv", "Susan Wong")
    CREATE_INVOICE("test_items.csv")
