#!/usr/bin/env python3

import os
import unittest

from basic_operations import _add_customers
from customer_model import *
from pathlib import Path
from peewee import *

current_path = Path.cwd()
src_path = current_path.with_name('src')

# os.chdir(src_path)


CUSTOMERS = [
    ("123", "Jurgen", "Muller", "337 Eichmann Locks", "1-615-598-8649 x975",
     "Jurgen@muller.net", "Active", 237),
    ("456", "Jens", "Blau", "765 Holstein Dr", "206.765.9087", "jb@mail.com",
     "active", 0),
    ("345", "Sven", "Kruse", "421 W. Galer", "206-908-2194", "svenk@wetten.de",
     "active", -10),
    ("0123", "Thor", "Weiss", "908 Howe St", "780-965-1243", "niemann@nichts.com",
     "active", 999),
    ("777", "Oskar", "Kratz", "67 Harald Dr", "905.987.3421", "ingen@vivs.no",
     "active", 999)
]


class CustomerModelTest(unittest.TestCase):
    """Tests that customers datbase
    is created"""

    def test_db_create(self):
        expected = src_path / 'customers.db'
        self.assertTrue(expected.exists())

    """Tests that the customer table
    was created"""

    def test_create_table(self):
        database = SqliteDatabase('customers.db')
        database.connect()
        expected = ['customer']
        self.assertIn('customer', database.get_tables())
        # database.close()

    # def test_add_customer(self):
    #     _add_customers(CUSTOMERS)
    #
    # def test_search_customers(self):
    #     expected = "[dict_values(['Jurgen', 'Muller', 'Jurgen@muller.net', '1-615-598-8649 x975'])]"
    #     self.assertEqual(expected, _search_customers(123))


if __name__ == '__main__':
    unittest.main()
