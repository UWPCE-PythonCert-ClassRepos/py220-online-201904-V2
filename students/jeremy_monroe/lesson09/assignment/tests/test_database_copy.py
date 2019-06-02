import pytest
import os

import database as l


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
        'user002': {'name': 'Maya Data', 'address': '4936 Elliot Avenue', 'phone_number': '206-777-1927', 'email': 'mdata@uw.edu'}
    }


def test_import_data():
    dir = os.path.dirname(os.path.abspath(__file__))
    added, errors = l.import_data(
        '../data/', "product.csv", "customers.csv", "rental.csv")
    for add in added:
        assert isinstance(add, int)
    for error in errors:
        assert isinstance(error, int)
    assert added == (10, 10, 9)
    assert errors == (0, 0, 0)


def test_show_available_products(_show_available_products):
    students_response = l.show_available_products()
    assert students_response == _show_available_products


def test_show_rentals(_show_rentals):
    students_response = l.show_rentals("prd010")
    assert students_response == _show_rentals

    with l.MONGO:
        TO_DROP = l.MONGO.connection
        TO_DROP.drop_database("assignment_05")
