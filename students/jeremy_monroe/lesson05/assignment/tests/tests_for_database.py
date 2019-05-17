""" Unit tests for database.py """

import pytest
import database as dab
import os


@pytest.fixture
def _show_available_products():
    return {
        'prd001': {'description': '60-inch TV stand', 'product_type': 'livingroom', 'quantity_available': '3'},
        'prd003': {'description': 'Acacia kitchen table', 'product_type': 'kitchen', 'quantity_available': '7'},
        'prd004': {'description': 'Queen bed', 'product_type': 'bedroom', 'quantity_available': '10'},
        'prd005': {'description': 'Reading lamp', 'product_type': 'bedroom', 'quantity_available': '20'},
        'prd006': {'description': 'Portable heater', 'product_type': 'bathroom', 'quantity_available': '14'},
        'prd008': {'description': 'Smart microwave', 'product_type': 'kitchen', 'quantity_available': '30'},
        'prd010': {'description': '60-inch TV', 'product_type': 'livingroom', 'quantity_available': '3'}
    }


@pytest.fixture
def _show_rentals():
    return {
            'user002': {'name': 'Maya Data', 'address': '4936 Elliot Avenue',
                    'phone_number': '206-777-1927', 'email': 'mdata@uw.edu'}
    }


def test_import_data():
    """ import """
    added, errors = dab.import_data('../data/', "product.csv",
                                    "customers.csv", "rental.csv")

    for add in added:
        assert isinstance(add, int)

    for error in errors:
        assert isinstance(error, int)

    assert added == (10, 10, 9)
    assert errors == (0, 0, 0)


def test_show_available_products(_show_available_products):
    """ available products """
    students_response = dab.show_available_products()
    assert students_response == _show_available_products


def test_show_rentals(_show_rentals):
    """ rentals """
    students_response = dab.show_rentals("prd010")
    assert students_response == _show_rentals


def test_parse_csv_input():
    """ Tests parse_csv_input function in database.py """
    test_infile = '../data/product.csv'
    test_parsed_file = dab.parse_csv_input(test_infile)

    assert 'Acacia kitchen table' in test_parsed_file[2]['description']

    test_infile_2 = '../data/customers.csv'
    test_parsed_file_2 = dab.parse_csv_input(test_infile_2)

    assert 'Shirlene Harris' in test_parsed_file_2[7]['name']
