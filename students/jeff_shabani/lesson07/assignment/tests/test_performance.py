#!/usr/bin/env python3

import unittest
from parallel import *
from linear import *
from pathlib import Path

current_path = Path.cwd()
src_path = current_path.with_name('src')


class PerformanceTesting(unittest.TestCase):

    def test_parallel_process_result_list(self):
        """
        test content of each results list tuple
        :return: tuple
        """
        remove_a_collection()
        expected = (9999, 0, 9999)
        self.assertEqual(expected, import_data_threading()[0][:3])
        self.assertEqual(expected, import_data_threading()[1][:3])


    def test_parallel_record_process_type(self):
        """
        Test that starting record processed counts are integers
        :return: tuple
        """
        remove_a_collection()
        self.assertIsInstance(import_data_threading()[0][0], int)
        self.assertIsInstance(import_data_threading()[1][0], int)

    def test_parallel_starting_record_count_type(self):
        """
        Test that starting record counts are integers
        """
        remove_a_collection()
        self.assertIsInstance(import_data_threading()[0][1], int)
        self.assertIsInstance(import_data_threading()[1][1], int)

    def test_parallel_post_load_count_type(self):
        """
        Test that post-load record counts are integers
        """
        remove_a_collection()
        self.assertIsInstance(import_data_threading()[0][2], int)
        self.assertIsInstance(import_data_threading()[1][2], int)


    def test_parallel_import_process_time_type_two(self):
        """
        test process in 2nd result tuple is a float
        :return: tuple
        """
        remove_a_collection()
        self.assertIsInstance(import_data_threading()[0][3], float)
        self.assertIsInstance(import_data_threading()[1][3], float)


if __name__ == '__main__':
    unittest.main()
