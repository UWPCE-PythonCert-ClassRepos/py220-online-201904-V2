#!/usr/bin/env python3
# pylint: disable = E1101, W0212, C0103, C0111, W0621
'''
grade lesson 5
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
    assert len(rentals_list) == 9999


def test_import_data(mongo_database):
    ''' import '''
    result = l.import_data(mongo_database, '', 'product.csv', 'customer.csv', 'rental.csv')

    assert result == ((9999, 9999, 9999), (0, 0, 0))


def test_show_available_products(_show_available_products, mongo_database):
    ''' available products '''
    l.import_data(mongo_database, '', 'product.csv', 'customer.csv', 'rental.csv')
    students_response = l.show_available_products(mongo_database)
    assert len(students_response) == 9999
    assert "P000001" in students_response
    assert "P010999" not in students_response



def test_show_rentals(_show_rentals, mongo_database):
    ''' rentals '''
    l.import_data(mongo_database, '', 'product.csv', 'customer.csv', 'rental.csv')
    students_response = l.show_rentals(mongo_database, 'prd002')
    expected = {'C000002': {'first_name': 'Blanca',
                            'last_name': 'Bashirian',
                            'address': '0193 Malvina Lake',
                            'phone_number': '(240)014-9496 x08349',
                            'email': 'Joana_Nienow@guy.org',
                            'status': 'Active',
                            'credit_limit': '689'},
                'C000004': {'first_name': 'Mittie',
                            'last_name': 'Turner',
                            'address': '996 Lorenza Points',
                            'phone_number': '1-324-023-8861 x025',
                            'email': 'Clair_Bergstrom@rylan.io',
                            'status': 'Active',
                            'credit_limit': '565'}}

    # assert len(students_response) == 0
    assert list(students_response.keys()) == ["C000002", "C000004"]
    assert students_response == expected


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
