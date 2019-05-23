#!/usr/bin/env python3
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
    file = Path.cwd().with_name('data') / file
    try:
        os.remove(file)
    except OSError:
        pass


def test_add_furniture(invoice_file, customer_name, item_code, item_description,
                       item_monthly_price):
    '''
    Testing adding furniture
    '''
    remove_file(invoice_file)
    l.add_furniture(invoice_file, 'Emilia', 'LR04', 'Sofa', 50.00)
    l.add_furniture(invoice_file, 'John', 'PS60', 'Chair', 150.00)

    assert os.path.isfile(invoice_file)

    with open(invoice_file, 'r') as csv_invoice:
        rows = csv_invoice.readlines()
        assert rows[0] == "Emilia, LR04, Sofa, 50.00\n"
        assert rows[1] == "John, PS60, Chair, 150.00\n"

        assert len(rows) == 2

    remove_file(invoice_file)



def test_single_customer(customer_name, invoice_file):
    '''
    Testing the single customer function
    '''
