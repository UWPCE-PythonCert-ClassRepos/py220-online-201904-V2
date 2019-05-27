"""
Jeremy Monroe tests for assignment_08

If they exist, please delete:

data/super_test_uncopyable_filename.csv
data/single_cust_test_file.csv
data/single_cust_partial_test_file.csv
data/append_to_existing_csv.csv

Otherwise these tests will not pass.
"""

import csv
import os
from random import randint
from functools import partial
from faker import Faker
from src import inventory as inv


FAKE = Faker()
RANDOM_ITEMS = ['Microwave', 'Couch', 'Lamp',
                'Blender', 'Faucet', 'Tupperware']

TEST_LIST = [['data/super_test_uncopyable_filename.csv',
              FAKE.name(), str(111+i),
              RANDOM_ITEMS[randint(0, (len(RANDOM_ITEMS)-1))],
              str(randint(50, 1000))] for i in range(10)]

TEST_ITEMS_FILENAME = 'data/test_items.csv'


def test_add_furniture():
    """
    Tests add_furniture function using a randomly generated list of customers,
    items, prices, and codes.

    Function should create file if it does not exist and append to it if it
    does.
    """
    # print(TEST_LIST)
    for item in TEST_LIST:
        inv.add_furniture(item[0], item[1], item[2], item[3], item[4])

    with open('data/super_test_uncopyable_filename.csv', 'r') as read_file:
        test_reader = list(csv.reader(read_file))
        for index, line in enumerate(test_reader):
            assert line == TEST_LIST[index][1:]

    os.remove('data/super_test_uncopyable_filename.csv')


def test_single_customer():
    """
    Tests the single_customer function using a randomly generated list of
    customers, items, prices, and codes.
    """
    test_single_customer_list = [[FAKE.name(),
                                  'data/single_cust_test_file.csv',
                                  TEST_ITEMS_FILENAME] for _ in range(10)]

    for customer in test_single_customer_list:
        temp_test_cust = inv.single_customer(customer[0], customer[1])
        temp_test_cust(customer[2])

    with open('data/single_cust_test_file.csv', 'r') as read_file:
        read_file_list = list(csv.reader(read_file))
        assert read_file_list[0] == [test_single_customer_list[0][0], 'LR01',
                                     'Small lamp', '7.50']

    os.remove('data/single_cust_test_file.csv')


def test_single_customer_partial():
    """
    Tests single_customer function using partial.
    """
    invoice_file = 'data/single_cust_partial_test_file.csv'
    test_cust_name = FAKE.name()
    test_cust_one = partial(inv.single_customer_partial,
                            test_cust_name,
                            invoice_file)

    test_cust_one(TEST_ITEMS_FILENAME)

    with open(invoice_file, 'r') as read_file:
        read_file_list = list(csv.reader(read_file))
        assert read_file_list[0] == [test_cust_name, 'LR01', 'Small lamp', '7.50']

    os.remove(invoice_file)


def test_append_to_exisiting_csv():
    """
    Tests my single_customer and add_customer to see if new records are added
    successfully to an existing csv file.
    """
    invoice_file = 'data/append_to_existing_csv.csv'
    test_append_list = [[FAKE.name(),
                                  invoice_file,
                                  TEST_ITEMS_FILENAME] for _ in range(10)]

    for customer in test_append_list:
        temp_test_cust = inv.single_customer(customer[0], customer[1])
        temp_test_cust(customer[2])

    for customer in test_append_list:
        temp_test_cust = inv.single_customer(customer[0], customer[1])
        temp_test_cust(customer[2])

    with open(invoice_file, 'r') as read_file:
        read_file_list = list(csv.reader(read_file))
        assert read_file_list[0] == [test_append_list[0][0], 'LR01',
                                     'Small lamp', '7.50']

        assert read_file_list[40] == [test_append_list[0][0], 'LR01',
                                     'Small lamp', '7.50']

    os.remove(invoice_file)