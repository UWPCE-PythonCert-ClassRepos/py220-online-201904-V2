#!/usr/bin/env python3

import os
import unittest

from parallel import *
from pathlib import Path
import tracemalloc

current_path = Path.cwd()
src_path = current_path.with_name('src')


class CustomerPerformance(unittest.TestCase):

    def test_parallel_import(self):
        tracemalloc.start()
        expected = (9999, 0, 9999)
        result = import_data_threading()
        self.assertEqual(expected, result)

    # def test_create_table(self):
    #     """Tests that the customer table
    #     was created"""
    #     database = SqliteDatabase('customers.db')
    #     database.connect()
    #     add_customer()
    #     expected = ['customer']
    #     self.assertIn('customer', database.get_tables())
    #     del_all_customers()
    #     database.close()
    #
    # def test_add_customer(self):
    #     """
    #     Test customers added from CSV"""
    #     database = SqliteDatabase('customers.db')
    #     database.connect()
    #     add_customer()
    #     self.assertEqual('Database has 10,000 total records.', total_records())
    #     database.close()
    #
    # def test_delete_customer(self):
    #     """
    #     Test deletion of single record"""
    #     database = SqliteDatabase('customers.db')
    #     database.connect()
    #     del_single_customer("C000001")
    #     self.assertEqual(None, print_customer_search("C000001"))
    #     database.close()
    #
    # def test_search_customers(self):
    #     """
    #     Test customer search function"""
    #     database = SqliteDatabase('customers.db')
    #     database.connect()
    #     add_customer()
    #     expected = "C000002 Blanca Bashirian Joana_Nienow@guy.org"
    #     self.assertEqual(expected, search_customers('C000002'))
    #     database.close()
    #
    # def test_get_table_columns(self):
    #     """
    #     Test function that lists all table columns
    #     """
    #     database = SqliteDatabase('customers.db')
    #     database.connect()
    #     add_customer()
    #     result = get_table_columns()
    #     expected = ['Unique_ID', 'customer_id', 'name', 'lastname',
    #                 'home_address', 'phone_number', 'email', 'status',
    #                 'credit_limit']
    #     self.assertListEqual(expected, result)
    #
    # def test_customer_limit_summary(self):
    #     """
    #     Test customer limit summary
    #     """
    #     database = SqliteDatabase('customers.db')
    #     database.connect()
    #     add_customer()
    #     expected = '98 customers have a credit limit >= 990 with and average limit of 995'
    #     self.assertEqual(expected, customer_limit_summary(990))
    #     database.close()
    #
    # def test_delete_all_records(self):
    #     """
    #     Test deleting all records
    #     """
    #     database = SqliteDatabase(src_path / 'customers.db')
    #     database.connect()
    #     add_customer()
    #     del_all_customers()
    #     self.assertEqual('Database has 0 total records.', total_records())
    #     database.close()
    #
    # def test_zdelete_database(self):
    #     """
    #     This is a simple utility to delete the test database.
    #     :return: database is deleted.
    #     """
    #     os.remove('customers.db')
    #     expected = current_path / 'customers.db'
    #     self.assertFalse(expected.exists())


if __name__ == '__main__':
    unittest.main()
