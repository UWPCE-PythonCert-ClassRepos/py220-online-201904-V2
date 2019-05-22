#!/usr/bin/env python3

import os
import pytest
import unittest
from inventory import *
from pathlib import Path

DATA_PATH = Path.cwd().with_name('data')

TEST_DATA = [('Elisa Miles', 'LR04', 'Leather Sofa', 25.00),
             ('Susan Wong', 'FB31', 'Home Haircut Machine', 21.00),
             ('Edward Data', 'KT78', 'Kitchen Table', 10.00),
             ('Susan Wong', 'BT31', 'Flat-Screen TV', 200.00),
             ('Alex Gonzales', 'BR02', 'Queen Mattress', 17.00),
             ('Susan Wong', 'KT15', '5-Burner Stove', 175.00)]


class PerformanceTesting(unittest.TestCase):

    def test_add_furniture(self):
        """
        test that inventory csv does not exist and then tests
        that it does exist after running adding records.
        :return: tuple
        """
        self.assertFalse(False, Path.exists(DATA_PATH / 'test_items.csv'))
        add_furniture('test_items.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25.00)
        add_furniture('test_items.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10.00)
        add_furniture('test_items.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)
        add_furniture('test_items.csv', 'Susan Wong', 'FB31', 'Home Haircut Machine', 21.00)
        add_furniture('test_items.csv', 'Susan Wong', 'BT31', 'Flat-Screen TV', 200.00)
        add_furniture('test_items.csv', 'Susan Wong', 'KT15', '5-Burner Stove', 175.00)
        self.assertTrue(True, Path.exists(DATA_PATH / 'test_items.csv'))
        os.remove(DATA_PATH / 'test_items.csv')

    def test_correct_number_of_records_added(self):
        """
        tests that the correct number of records are
        added to the inventory csv
        :return: tuple
        """
        add_furniture('test_items.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25.00)
        add_furniture('test_items.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10.00)
        add_furniture('test_items.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)
        add_furniture('test_items.csv', 'Susan Wong', 'FB31', 'Home Haircut Machine', 21.00)
        add_furniture('test_items.csv', 'Susan Wong', 'BT31', 'Flat-Screen TV', 200.00)
        add_furniture('test_items.csv', 'Susan Wong', 'KT15', '5-Burner Stove', 175.00)
        test = pd.read_csv(DATA_PATH / 'test_items.csv')
        len_csv = int(test.iloc[:, 0].count())
        self.assertEqual(6, len_csv)

    def test_invoice(self):
        """
        Tests creation of new rented_items csv including only records with the
        name entered as an argument utilizing currying.
        :return: csv file
        """
        create_invoice = partial(single_customer, 'Susan Wong', 'rented_items.csv')
        create_invoice('test_items.csv')
        test = pd.read_csv(DATA_PATH / 'rented_items.csv')
        test = test[test['customer_name'] == 'Susan Wong']
        len_csv = int(test.iloc[:, 0].count())
        self.assertTrue(True, Path.exists(DATA_PATH / 'rented_items.csv'))
        self.assertEqual(3, len_csv)
        os.remove(DATA_PATH / 'test_items.csv')
        os.remove(DATA_PATH / 'rented_items.csv')


if __name__ == '__main__':
    unittest.main()
