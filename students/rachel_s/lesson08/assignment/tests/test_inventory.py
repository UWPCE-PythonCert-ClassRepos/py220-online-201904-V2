"""
    Autograde Lesson 8 assignment

"""

import csv
import os
from pathlib import Path
import pytest
from loguru import logger
import inventory as l


def test_add_furniture():
    my_path = Path('test.txt')
    logger.debug('If the test.txt file already exists, remove it.')
    if my_path.is_file():
        os.remove(my_path)
    logger.debug('Make sure the file is gone.')
    assert not my_path.is_file()
    logger.debug('Test file creation on first addition')
    l.add_furniture(
        'test.txt',
        'Jim',
        '001',
        'spaceship',
        2000
    )
    assert my_path.is_file()
    logger.debug('Test subsequent additions.')
    l.add_furniture(
        'test.txt',
        'Naomi',
        '002',
        'antimatter',
        12000
    )
    l.add_furniture(
        'test.txt',
        'Amos',
        '003',
        'wrench',
        11
    )
    test_data = []
    with open(my_path) as f:
        reader = csv.reader(f)
        for line in reader:
            test_data.append(line)
    assert test_data[0] == ['Jim', '001', 'spaceship', '2000']
    assert test_data[1] == ['Naomi', '002', 'antimatter', '12000']
    assert test_data[2] == ['Amos', '003', 'wrench', '11']

    logger.debug('Cleaning up test.txt')
    if my_path.is_file():
        os.remove(my_path)

def test_single_customer():
    my_path = Path('test.txt')
    test_result = [
        ['Alex', 'LR01', 'Small lamp', '7.50'],
        ['Alex', 'LR02', 'Television', '28.00'],
        ['Alex', 'BR07', 'LED lamp', '5.50'],
        ['Alex', 'KT08', 'Basic refrigerator', '40.00']
    ]
    logger.debug('If test.txt exists, delete it.')
    if my_path.is_file():
        os.remove(my_path)
    test_func = l.single_customer('Alex', 'test.txt')
    test_func('../data/test_items.csv')
    test_data = []
    with open(my_path) as f:
        reader = csv.reader(f)
        for line in reader:
            test_data.append(line)
    assert test_data == test_result
