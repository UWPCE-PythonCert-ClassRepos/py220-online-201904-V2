#!/usr/bin/env python3
#pylint: disable=C0103, W0621
'''
Inventory management through functional programming
'''
import csv
import logging
from functools import partial
from pathlib import Path
from timeit import timeit
# from line_profiler import LineProfiler


logging.basicConfig(filename='inventory.log', level=logging.DEBUG)

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
    logging.info('Furnature added')


def add_test_data(invoice_file):
    '''
    Populating the test date into the file.
    '''
    logging.info('Adding test data')

    add_furniture(invoice_file, 'Elisa Miles', 'LR04', 'Leather Sofa',
                  '25.00')
    add_furniture(invoice_file, 'Edward Data', 'KT78', 'Kitchen Table',
                  '10.00')
    add_furniture(invoice_file, 'Alex Gonzales', 'BR02', 'Queen Mattress',
                  '17.00')


def single_customer(customer_name, invoice_file):
    '''
    Bulk processes a list of items that have been rented to a single customer.
    '''
    def add_rentals(rental_items):
        with open(rental_items) as rental_csv:
            reader = csv.reader(rental_csv)
            add_item = partial(add_furniture, invoice_file=invoice_file,
                               customer_name=customer_name)

            for row in reader:
                add_item(item_code=row[0], item_description=row[1],
                         item_monthly_price=row[2])
    logging.info('Rental data added')
    return add_rentals


if __name__ == '__main__':

    invoice_file = Path.cwd().with_name('data') / 'invoice_file.csv'
    add_test_data(invoice_file)
    test_items = invoice = Path.cwd().with_name('data') / 'test_items.csv'
    test_customer = single_customer('Susan Wong', invoice_file)
    test_customer(test_items)

    print(timeit('add_test_data(invoice_file)', globals=globals(), number=1))
    print(timeit('add_test_data(invoice_file)', globals=globals(), number=10))

    # lp = LineProfiler()
    # lp_wrapper = lp(add_test_data(invoice_file))
    # lp_wrapper()
    # lp.print_stats()
