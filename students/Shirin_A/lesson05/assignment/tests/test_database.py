"""
grade lesson 5
"""
# pylint: disable=redefined-outer-name,W0212,E0401 
import os
import pytest
import database as l


@pytest.fixture(scope="function")
def mongo_database():
    """Creates a MongoDB. """
    mongo = l.MongoDBConnection()
    with mongo:

        database = mongo.connection.media
        yield database
        l.clear_data(database)

@pytest.fixture
def _show_available_products():
    return {
        'prd001':{'description': '60-inch TV stand', 'product_type': 'livingroom',
                  'quantity_available':'3'},
        'prd003':{'description': 'Acacia kitchen table', 'product_type': 'kitchen',
                  'quantity_available':'7'},
        'prd004':{'description': 'Queen bed', 'product_type': 'bedroom',
                  'quantity_available':'10'},
        'prd005':{'description': 'Reading lamp', 'product_type': 'bedroom',
                  'quantity_available':'20'},
        'prd006':{'description': 'Portable heater', 'product_type': 'bathroom',
                  'quantity_available':'14'},
        'prd008':{'description': 'Smart microwave', 'product_type': 'kitchen',
                  'quantity_available':'30'},
        'prd010':{'description': '60-inch TV', 'product_type': 'livingroom',
                  'quantity_available':'3'}
        }

@pytest.fixture
def _show_rentals():
    return {
        'user004':{'name': 'Flor Matatena', 'address': '885 Boone Crockett Lane',
                   'phone_number': '206-414-2629', 'email': 'matseattle@pge.com'}
                }


def test_import_csv():
    """docstring"""

    rentals_list = l._import_csv("../data/rental.csv")
    assert {'product_id': 'prd002', 'user_id': 'user008'} in rentals_list
    assert len(rentals_list) == 9


def test_import_data(mongo_database):
    ''' import '''
    data_dir = os.path.dirname(os.path.abspath(__file__))
    added, errors = l.import_data(mongo_database, data_dir, "../data/product.csv",
                                  "../data/customers.csv", "../data/rental.csv")
    for add in added:
        assert isinstance(add, int)
    for error in errors:
        assert isinstance(error, int)
    assert added == (10, 10, 9)
    assert errors == (0, 0, 0)

def test_show_available_products(mongo_database, _show_available_products):
    """ available products """
    l.import_data(mongo_database, '../data', '../data/product.csv',
                  '../data/customers.csv', '../data/rental.csv')
    students_response = l.show_available_products(mongo_database)
    assert students_response == _show_available_products

def test_show_rentals(mongo_database, _show_rentals):
    """ rentals """
    l.import_data(mongo_database, '../data', '../data/product.csv',
                  '../data/customers.csv', '../data/rental.csv')
    students_response = l.show_rentals(mongo_database, "prd003")
    assert students_response == _show_rentals
