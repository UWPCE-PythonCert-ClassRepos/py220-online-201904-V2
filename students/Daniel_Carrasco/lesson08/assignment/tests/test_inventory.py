#!/usr/bin/env python3
# pylint: disable=W0613, W0611
'''
    Autograde Lesson 8 assignment
'''

import os
from pathlib import Path
import pytest
import inventory as l


def remove_file(file):
    '''
    Removing any data that exists
    '''
    file = Path.cwd().with_name('data') / 'invoice_file.csv'
    try:
        os.remove(file)
    except OSError:
        pass


def test_add_furniture():
    '''
    Testing adding furniture
    '''
    invoice_file = Path.cwd().with_name('data') / 'invoice_file.csv'
    remove_file(invoice_file)
    l.add_furniture(invoice_file, 'Emilia', 'LR04', 'Sofa', 50.0)
    l.add_furniture(invoice_file, 'John', 'PS60', 'Chair', 150.0)

    assert os.path.isfile(invoice_file)

    with open(invoice_file, 'r') as csv_invoice:
        rows = csv_invoice.readlines()
        assert rows[0] == 'Emilia,LR04,Sofa,50.0\n'
        assert rows[1] == 'John,PS60,Chair,150.0\n'

        assert len(rows) == 2

    remove_file(invoice_file)


def test_single_customer():
    '''
    Testing the single customer function
    '''
    invoice_file = Path.cwd().with_name('data') / 'invoice_file.csv'
    rental_file = Path.cwd().with_name('data') / 'test_items.csv'
    customer = l.single_customer('Amy Sutton', invoice_file)
    customer(rental_file)
    with open(invoice_file, 'r') as f:
        items = f.readlines()
        assert items[0] == 'Amy Sutton,LR01,Small lamp,7.50\n'

# def test_single_customer():
    # customer_file = inv.single_customer("Lisa Miles", INVOICE_FILE)
    # customer_file(RENTAL_FILE)
    # with open(INVOICE_FILE, 'r') as file:
        # items = file.readlines()
        # assert items[0] == "Lisa Miles, LR04, Leather Sofa, 25.00\n"
        # assert len(items) == 2
