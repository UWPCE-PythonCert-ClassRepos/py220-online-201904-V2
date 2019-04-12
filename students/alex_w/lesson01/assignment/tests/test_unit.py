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


"""Main Tests"""

def test_main_menu(monkeypatch):
    """Tests user input"""
    assert main_menu('1') == add_new_item
    assert main_menu('2') == item_info
    assert main_menu('q') == exit_program


def test_get_price():
    """Tests that get_price returns the expected"""
    assert get_price(200) == 200
    assert get_price(2000) == 2000
    assert get_price(-200) == 2100
    assert get_price(-2000) == -2000


def test_new_item_furniture(monkeypatch, mocker):
    """Tests adding a new item to Furniture"""
    product_code = 12345
    description = 'Table'
    market_price = 100
    rental_price = 25
    material = 'Wood'
    size = 'L'
    user_input = [size, material, 'y', rental_price, description, product_code]


def test_new_item_electric_app(monkeypatch, mocker):
    """Tests adding a new item of type ElectricAppliances"""
    product_code = 12345
    description = 'Microwave'
    market_price = 100
    rental_price = 25
    brand = 'LG'
    voltage = '120'
    user_input = [voltage, brand, 'y', 'n',
                  rental_price, description, product_code]


def test_item_info(monkeypatch):
    """Tests that item_info returns expected values"""
    expected_return = (f'product_code:123\n'
                       f'description:Chair\n'
                       f'market_price:200\n'
                       f'rental_price:25\n')
    FULL_INVENTORY['123'] = {'product_code': '123',
                             'description': 'Chair',
                             'market_price': '200',
                             'rental_price': '25'}


"""Inventory management module tests"""

def test_get_latest_price_market():
    """Tests that get latest price returns"""
    assert get_latest_price(200) == 200
    assert get_latest_price(2000) == 2000
    assert get_latest_price(-200) == -200
    assert get_latest_price(-2000) == -2000
