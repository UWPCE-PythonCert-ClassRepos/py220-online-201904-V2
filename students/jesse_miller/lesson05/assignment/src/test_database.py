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
        'P000001': {'description': 'Chair Red leather', 'product_type': 'livingroom',
                    'quantity_available': '21'},
        'P000002': {'description': 'Table Oak', 'product_type': 'livingroom',
                    'quantity_available': '4'},
        'P000003': {'description': 'Couch Green cloth', 'product_type': 'livingroom',
                    'quantity_available': '10'},
        'P000004': {'description': 'Dining table Plastic', 'product_type': 'Kitchen',
                    'quantity_available': '23'},
        'P000005': {'description': 'Stool Black ash', 'product_type': 'Kitchen',
                    'quantity_available': '12'}
        }

@pytest.fixture
def _show_rentals():
    return {
        'C000001': {'name': 'Shea Boehm', 'address': '3343 Sallie Gateway',
                    'phone_number': '508.104.0644', 'email': 'Alexander.Weber@monroe.com'},
        'C000003': {'name': 'Elfrieda Skiles', 'address': '3180 Mose Row',
                    'phone_number': '839)825-0058', 'email': 'Mylene_Smitham@hannah.co.uk'}
        }


def test_import_csv():
    rentals_list = l._import_csv('rental.csv')

    assert {'product_id': 'prd002', 'user_id': 'user008'} in rentals_list
    assert len(rentals_list) == 9


def test_import_data(mongo_database):
    ''' import '''
    result = l.import_data(mongo_database, '', 'product.csv', 'customers.csv', 'rental.csv')

    assert result == ((10, 10, 9), (0, 0, 0))


def test_show_available_products(_show_available_products):
    ''' available products '''
    result = l.import_data(mongo_database, '', 'product.csv', 'customers.csv', 'rental.csv')
    students_response = l.show_available_products(result)
    assert students_response == _show_available_products


def test_show_rentals(_show_rentals):
    ''' rentals '''
    result = l.import_data(mongo_database, '', 'product.csv', 'customers.csv', 'rental.csv')
    students_response = l.show_rentals(result, 'P000003')
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
