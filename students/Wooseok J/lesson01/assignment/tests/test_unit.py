from unittest import TestCase
from unittest.mock import patch, MagicMock
from inventory_class import Inventory
from furniture_class import Furniture
from electric_appliances_class import Electric_Appliances
from market_prices import get_latest_price
from main import main_menu
from main import get_price
from main import add_new_item
from main import item_info
from main import exit_program
from main import FULL_INVENTORY


def test_main_menu(monkeypatch):
    assert main_menu('1') == add_new_item
    assert main_menu('2') == item_info
    assert main_menu('q') == exit_program


def test_get_price():
    assert get_price(200) == 200
    assert get_price(2000) == 2000
    assert get_price(-200) == 2100
    assert get_price(-2000) == -2000


def test_new_item_furniture(monkeypatch, mocker):
    product_code = 199
    description = 'Table'
    market_price = 300
    rental_price = 60
    material = 'Wood'
    size = 'L'
    user_input = [size, material, 'y', rental_price, description, product_code]


def test_new_item_electric_app(monkeypatch, mocker):
    product_code = 198
    description = 'Microwave'
    market_price = 200
    rental_price = 50
    brand = 'Samsung'
    voltage = '220'
    user_input = [voltage, brand, 'y', 'n',
                  rental_price, description, product_code]


def test_item_info(monkeypatch):
    expected_return = (f'product_code:199\n'
                       f'description:Chair\n'
                       f'market_price:300\n'
                       f'rental_price:60\n')
    FULL_INVENTORY['123'] = {'product_code': '199',
                             'description': 'Chair',
                             'market_price': '300',
                             'rental_price': '65'}

def test_get_latest_price_market():
    assert get_latest_price(200) == 200
    assert get_latest_price(2000) == 2000
    assert get_latest_price(-200) == -200
    assert get_latest_price(-2000) == -2000