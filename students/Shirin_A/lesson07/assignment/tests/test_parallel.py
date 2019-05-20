"""
grade lesson 5
"""

# pylint: disable=E0401

import pytest
import parallel as p
 
@pytest.fixture(scope="function")
def _mongo_database():
    """Creates a MongoDB. """
    mongo = p.MongoDBConnection()
    with mongo:

        database = mongo.connection.media
        yield database
        p.clear_data(database)

@pytest.fixture
def _show_available_products():
    return {
        'P000001':{'description': 'Chair Red leather', 'product_type': 'Livingroom',
                   'quantity_available':'21'},
        'P0000003':{'description': 'Couch Green cloth', 'product_type': 'Livingroom',
                    'quantity_available':'10'},
        'P000004':{'description': 'Dining table Plastic', 'product_type': 'Kitchen',
                   'quantity_available':'23'},
        'P000005':{'description': 'Stool Black ash', 'product_type': 'Kitchen',
                   'quantity_available':'12'},
        'P000006':{'description': 'Chair Red leather', 'product_type': 'Livingroom',
                   'quantity_available':'21'},
        'P000008':{'description': 'Couch Green cloth', 'product_type': 'Livingroom',
                   'quantity_available':'10'},
        }

@pytest.fixture
def _show_rentals():
    return {
        'C000010':{'Name': 'Ruthe', 'address': '186 Theodora Parkway',
                   'phone_number':'1-642-296-4711 x359', 'email': 'Oren@sheridan.name'}
                }


def test_import_csv():
    "docstring"
    products_list = p.import_csv("../data/product.csv")
    assert len(products_list) == 9999

def test_add_bulk_data(_mongo_database):
    """Docstring"""
    results_dict = {}
    p.add_bulk_data(results_dict, _mongo_database.rentals, "", "../data/rental.csv")

    assert results_dict["rentals"][0] == 9999
    assert results_dict["rentals"][1] == 0
    assert results_dict["rentals"][2] == 9999
    assert isinstance(results_dict["rentals"][3], float)


def test_import_data(_mongo_database):
    """Import"""

    result = p.import_data(_mongo_database, "", "../data/product.csv",
                           "../data/customer.csv", "../data/rental.csv")
    assert result[0][0] == 9999
    assert result[0][1] == 0
    assert result[0][2] == 9999
    assert isinstance(result[0][3], float)
    assert result[1][0] == 9999
    assert result[1][1] == 0
    assert result[1][2] == 9999
    assert isinstance(result[1][3], float)

def test_show_available_products(_mongo_database, _show_available_products):
    ''' available products '''
    p.import_data(_mongo_database, '../data', '../data/product.csv',
                  '../data/customer.csv', '../data/rental.csv')
    students_response = p.show_available_products(_mongo_database)
    assert len(students_response) == 9999

    assert "P000001" in students_response

    assert "P010999" not in students_response


def test_show_rentals(_mongo_database, _show_rentals):
    """ rentals """
    p.import_data(_mongo_database, '../data', '../data/product.csv',
                  '../data/customer.csv', '../data/rental.csv')
    students_response = p.show_rentals(_mongo_database, "P000005")
    assert students_response == _show_rentals
