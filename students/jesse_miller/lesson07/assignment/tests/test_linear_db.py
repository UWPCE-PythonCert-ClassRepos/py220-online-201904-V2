#!/usr/bin/env python3
# pylint: disable = E1101, W0212, C0103, C0111, W0621, E0401
'''
grade lesson 7
'''

import pytest
import linear_db as l


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


def test_import_csv():
    rentals_list = l._import_csv('rental.csv')
    assert len(rentals_list) == 9999


def test_import_data(mongo_database):
    ''' import '''
    result = l.import_data(mongo_database, '', 'product.csv', 'customer.csv', 'rental.csv')

    assert result == ((9999, 9999, 9999), (0, 0, 0))


def test_show_available_products(mongo_database):
    ''' available products '''
    l.import_data(mongo_database, '', 'product.csv', 'customer.csv', 'rental.csv')
    students_response = l.show_available_products(mongo_database)
    assert len(students_response) == 9999
    assert 'P000001' in students_response
    assert 'P010999' not in students_response



def test_show_rentals(mongo_database):
    l.import_data(mongo_database, '', 'product.csv', 'customer.csv', 'rental.csv')
    result = l.show_rentals(mongo_database, 'P000004')

    assert len(result) == 2
    assert list(result.keys()) == ['C000002', 'C000004']


def test_clear_data(mongo_database):
    '''
    Testing database clearing.
    '''
    l.import_data(mongo_database, '', 'product.csv', 'customer.csv', 'rental.csv')

    result = mongo_database.list_collection_names()
    assert result == ['products', 'rentals', 'customers']

    l.clear_data(mongo_database)
    result2 = mongo_database.list_collection_names()
    assert result2 == []
