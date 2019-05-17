"""
grade lesson 5
"""

import os
from pathlib import Path
import pytest
import unittest
import database as l


@pytest.fixture
def _show_available_products():
    return [{'product_id': 'prd001', 'description': '60-inch TV stand', 'product_type': 'livingroom',
             'quantity_available': 3},
            {'product_id': 'prd003', 'description': 'Acacia kitchen table', 'product_type': 'kitchen',
             'quantity_available': 7},
            {'product_id': 'prd004', 'description': 'Queen bed', 'product_type': 'bedroom', 'quantity_available': 10},
            {'product_id': 'prd005', 'description': 'Reading lamp', 'product_type': 'bedroom',
             'quantity_available': 20},
            {'product_id': 'prd006', 'description': 'Portable heater', 'product_type': 'bathroom',
             'quantity_available': 14},
            {'product_id': 'prd008', 'description': 'Smart microwave', 'product_type': 'kitchen',
             'quantity_available': 30},
            {'product_id': 'prd010', 'description': '60-inch TV', 'product_type': 'livingroom',
             'quantity_available': 3}]


@pytest.fixture
def _show_rentals():
    return {
        'user_id': 'user010', 'name': 'Jose Garza', 'address': '2717 Raccoon Run', 'phone_number': '206-946-8200',
        'email': 'joegarza@boeing.com'}


def test_import_data():
    """ import """
    data_dir = Path.cwd().with_name('data')
    added, errors = l.import_data(data_dir, "product.csv", "customers.csv", "rental.csv")

    for add in added:
        assert isinstance(add, int)

    for error in errors:
        assert isinstance(error, int)

    assert added == (10, 10, 9)
    assert errors == (0, 0, 0)


def test_show_available_products(_show_available_products):
    """ available products """
    students_response = l.show_available_products()
    assert students_response == _show_available_products


def test_show_rentals(_show_rentals):
    """ rentals """
    students_response = l.show_rentals("prd001")
    assert students_response == _show_rentals
