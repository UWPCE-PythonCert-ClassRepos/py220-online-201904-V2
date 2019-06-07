# pylint: disable=W0212, W0621, W0212, C0111, C0103, E0401
import pytest
import database as d


@pytest.fixture(scope='function')
def mongo_database():
    '''
    Creates a MongoDB.
    '''
    mongo = d.MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        test_utilities = d.Database()

        yield (db, test_utilities)

        test_utilities.clear_data(db)


def test_import_csv(mongo_database):
    products_list = mongo_database[1]._import_csv('product.csv')

    assert len(products_list) == 9999


def test_import_data(mongo_database):
    result = mongo_database[1].import_data(mongo_database[0],
                                           '',
                                           'product.csv',
                                           'customer.csv',
                                           'rental.csv')

    assert result == ((9999, 9999, 9999), (0, 0, 0))


def test_show_available_products(mongo_database):
    mongo_database[1].import_data(mongo_database[0],
                                  '',
                                  'product.csv',
                                  'customer.csv',
                                  'rental.csv')

    result = mongo_database[1].show_available_products(mongo_database[0])

    assert len(result) == 9999
    assert 'P000001' in result
    assert 'P010999' not in result


def test_show_rentals(mongo_database):
    mongo_database[1].import_data(mongo_database[0],
                                  '',
                                  'product.csv',
                                  'customer.csv',
                                  'rental.csv')

    result = mongo_database[1].show_rentals(mongo_database[0], 'P000004')

    assert len(result) == 2
    assert list(result.keys()) == ['C000002', 'C000004']


def test_clear_data(mongo_database):
    mongo_database[1].import_data(mongo_database[0],
                                  '',
                                  'product.csv',
                                  'customer.csv',
                                  'rental.csv')

    result = mongo_database[0].list_collection_names()

    assert result == ['products', 'rentals', 'customers']

    mongo_database[1].clear_data(mongo_database[0])
    result2 = mongo_database[0].list_collection_names()
    assert result2 == []
