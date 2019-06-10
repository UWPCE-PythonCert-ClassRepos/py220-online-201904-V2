import pytest
import database as db


@pytest.fixture
def _test_parse_csv_input():
    return [
        {'user_id': 'C000264', 'name': 'Cheryl Stream',
         'address': '3362 Sallie Gateway', 'phone_number': '508.104.0644 x4995',
         'email': 'Alexander.Weber@monroe.com', 'product_id': 'P000259'},
        {'user_id': 'C000765', 'name': 'Many Things',
         'address': '3362 Sallie Gateway', 'phone_number': '508.104.0644 x4995',
         'email': 'Alexander.Weber@monroe.com', 'product_id': 'P000259'},
        {'user_id': 'C000763', 'name': 'Quality Sheen',
         'address': '3362 Sallie Gateway', 'phone_number': '508.104.0644 x4995',
         'email': 'Alexander.Weber@monroe.com', 'product_id': 'P000259'},
        {'user_id': 'C000543', 'name': 'Happy Tree',
         'address': '3362 Sallie Gateway', 'phone_number': '508.104.0644 x4995',
         'email': 'Alexander.Weber@monroe.com', 'product_id': 'P000259'},
        {'user_id': 'C000876', 'name': 'Wandering Stream',
         'address': '3362 Sallie Gateway', 'phone_number': '508.104.0644 x4995',
         'email': 'Alexander.Weber@monroe.com', 'product_id': 'P000259'},
        {'user_id': 'C000872', 'name': 'Alpaca Steve',
         'address': '3362 Sallie Gateway', 'phone_number': '508.104.0644 x4995',
         'email': 'Alexander.Weber@monroe.com', 'product_id': 'P000259'}
    ]


def test_parse_csv_input(_test_parse_csv_input):
    parsed_csv = db.parse_csv_input('../data/test_rental.csv')

    assert parsed_csv == _test_parse_csv_input


def test_import_data():
    dir_name = '../data/'
    success_count, error_count = db.import_data(
        dir_name, 'test_product.csv', 'test_customer.csv', 'test_rental.csv')

    assert success_count == (12, 16, 6)
    assert error_count == (0, 0, 0)


def test_show_available_products():
    available_products = db.show_available_products()

    assert len(available_products) == 12


def test_show_rentals():
    show_rentals = db.show_rentals('P000259')

    assert len(show_rentals) == 6

    with db.MONGO:
        TO_DROP = db.MONGO.connection
        TO_DROP.drop_database("assignment_10")