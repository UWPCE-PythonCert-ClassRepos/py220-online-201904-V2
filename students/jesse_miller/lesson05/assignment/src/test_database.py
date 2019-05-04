#!/usr/bin/env python3
# pylint: disable = E1101, W0212, C0103, C0111, W0621
'''
grade lesson 5
'''

import pytest
import database as l


@pytest.fixture(scope='function')
def mongo_database():
    '''
    Creating the MongoDB for testing.
    '''
    mongo = l.MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        yield db

        l.clear_data(db)


@pytest.fixture
def _show_available_products():
    return {
        'prd001': {
            'description': '60-inch TV stand',
            'product_type': 'livingroom',
            'quantity_available': '3',
        },
        'prd003': {
            'description': 'Acacia kitchen table',
            'product_type': 'kitchen',
            'quantity_available': '7',
        },
        'prd004': {
            'description': 'Queen bed',
            'product_type': 'bedroom',
            'quantity_available': '10',
        },
        'prd005': {
            'description': 'Reading lamp',
            'product_type': 'bedroom',
            'quantity_available': '20',
        },
        'prd006': {
            'description': 'Portable heater',
            'product_type': 'bathroom',
            'quantity_available': '14',
        },
        'prd008': {
            'description': 'Smart microwave',
            'product_type': 'kitchen',
            'quantity_available': '30',
        },
        'prd010': {
            'description': '60-inch TV',
            'product_type': 'livingroom',
            'quantity_available': '3',
        },
    }

@pytest.fixture
def _show_rentals():
    ''' Expected output for show rentals call '''
    return {
        'user005': {
            'name': 'Dan Sounders',
            'address': '861 Honeysuckle Lane',
            'phone_number': '206-279-1723',
            'email': 'soundersoccer@mls.com',
        },
        'user008': {
            'name': 'Shirlene Harris',
            'address': '4329 Honeysuckle Lane',
            'phone_number': '206-279-5340',
            'email': 'harrisfamily@gmail.com',
        },
    }


def test_import_csv():
    rentals_list = l._import_csv('rental.csv')

    assert {'product_id': 'prd002', 'user_id': 'user008'} in rentals_list
    assert len(rentals_list) == 9


def test_import_data(mongo_database):
    ''' import '''
    result = l.import_data(mongo_database, '', 'product.csv', 'customers.csv', 'rental.csv')

    assert result == ((10, 10, 9), (0, 0, 0))


def test_show_available_products(_show_available_products, mongo_database):
    ''' available products '''
    l.import_data(mongo_database, '', 'product.csv', 'customers.csv', 'rental.csv')
    students_response = l.show_available_products(mongo_database)
    assert students_response == _show_available_products


def test_show_rentals(_show_rentals, mongo_database):
    ''' rentals '''
    l.import_data(mongo_database, '', 'product.csv', 'customers.csv', 'rental.csv')
    students_response = l.show_rentals(mongo_database, 'P000003')
    assert students_response == _show_rentals


def test_clear_data(mongo_database):
    '''
    Testing database clearing.
    '''
    l.import_data(mongo_database, '', 'product.csv', 'customers.csv', 'rental.csv')

    result = mongo_database.list_collection_names()
    assert result == ['products', 'rentals', 'customers']

    l.clear_data(mongo_database)
    result2 = mongo_database.list_collection_names()
    assert result2 == []
