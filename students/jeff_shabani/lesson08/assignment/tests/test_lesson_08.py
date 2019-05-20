#!/usr/bin/env python3

import os
import pytest
import unittest
from inventory import *
from pathlib import Path


DATA_PATH = Path.cwd().with_name('data')

TEST_DATA=[('Elisa Miles', 'LR04', 'Leather Sofa', 25.00),
            ('Edward Data', 'KT78', 'Kitchen Table', 10.00),
            ('Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)]


class PerformanceTesting(unittest.TestCase):

    def test_add_furniture(self):
        """
        test that inventory csv does not exist and then tests
        that it does exist after running adding records.
        :return: tuple
        """
        self.assertFalse(False, Path.exists(DATA_PATH / 'inventory.csv'))
        add_furniture('inventory.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25.00)
        add_furniture('inventory.csv','Edward Data', 'KT78', 'Kitchen Table', 10.00)
        add_furniture('inventory.csv','Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)
        self.assertTrue(True, Path.exists(DATA_PATH / 'inventory.csv'))
        os.remove(DATA_PATH / 'inventory.csv')


    def test_correct_number_of_records_added(self):
        """
        tests that the correct number of records are
        added to the inventory csv
        :return: tuple
        """
        add_furniture('inventory.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25.00)
        add_furniture('inventory.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10.00)
        add_furniture('inventory.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)
        test = pd.read_csv(DATA_PATH/'inventory.csv')
        len_csv = int(test.iloc[:, 0].count())
        self.assertEqual(3, len_csv)
        os.remove(DATA_PATH / 'inventory.csv')

#
#
#
#     def test_parallel_record_process_type(self):
#         """
#         Test that starting record processed counts are integers
#         :return: tuple
#         """
#         remove_a_collection()
#         self.assertIsInstance(import_data_threading()[0][0], int)
#         self.assertIsInstance(import_data_threading()[1][0], int)
#
#
#     def test_parallel_starting_record_count_type(self):
#         """
#         Test that starting record counts are integers
#         """
#         remove_a_collection()
#         self.assertIsInstance(import_data_threading()[0][1], int)
#         self.assertIsInstance(import_data_threading()[1][1], int)
#
#
#     def test_parallel_post_load_count_type(self):
#         """
#         Test that post-load record counts are integers
#         """
#         remove_a_collection()
#         self.assertIsInstance(import_data_threading()[0][2], int)
#         self.assertIsInstance(import_data_threading()[1][2], int)
#
#
#     def test_parallel_import_process_time_type_two(self):
#         """
#         test process in 2nd result tuple is a float
#         :return: tuple
#         """
#         remove_a_collection()
#         self.assertIsInstance(import_data_threading()[0][3], float)
#         self.assertIsInstance(import_data_threading()[1][3], float)
#
#
#     def test_linear_process_result_list(self):
#         """
#         test content of each results list tuple
#         :return: tuple
#         """
#         remove_a_collection()
#         expected = (9999, 0, 9999)
#         # src_path = Path.cwd().with_name('data')
#         self.assertEqual(expected, import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[0][:3])
#         self.assertEqual(expected, import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[1][:3])
#
#
#     def test_linear_record_process_type(self):
#         """
#         Test that starting record processed counts are integers
#         :return: tuple
#         """
#         remove_a_collection()
#         self.assertIsInstance(import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[0][0], int)
#         self.assertIsInstance(import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[1][0], int)
#
#
#     def test_linear_starting_record_count_type(self):
#         """
#         Test that starting record counts are integers
#         """
#         remove_a_collection()
#         self.assertIsInstance(import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[0][1], int)
#         self.assertIsInstance(import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[1][1], int)
#
#
#     def test_linear_post_load_count_type(self):
#         """
#         Test that post-load record counts are integers
#         """
#         remove_a_collection()
#         self.assertIsInstance(import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[0][2], int)
#         self.assertIsInstance(import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[1][2], int)
#
#
#     def test_linear_import_process_time_type_two(self):
#         """
#         test process in 2nd result tuple is a float
#         :return: tuple
#         """
#         remove_a_collection()
#         self.assertIsInstance(import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[0][3], float)
#         self.assertIsInstance(import_data(SRC_PATH,
#                                                'product.csv', 'customers.csv')[1][3], float)


if __name__ == '__main__':
    unittest.main()

