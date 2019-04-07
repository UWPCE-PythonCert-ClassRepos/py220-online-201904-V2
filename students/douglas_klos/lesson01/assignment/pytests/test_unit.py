#pylint: disable=W0143
"""Pytest cases for inventory management module and main"""

# Douglas Klos
# April 3rd, 2019
# Python 220, Lesson 01
# test_unit.py


import sys
from contextlib import contextmanager
from io import StringIO
import pytest

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price

from main import main_menu
from main import get_price
from main import add_new_item
from main import item_info
from main import exit_program
from main import FULL_INVENTORY


@contextmanager
def captured_output():
    """Context manager to capture stdout for analysis"""
    new_out = StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


# ------------------- Main tests ------------------ #

def test_main_menu(monkeypatch):
    """Tests that main_menu accepts user input
    and returns corrent function calls

    """
    assert main_menu('1') == add_new_item
    assert main_menu('2') == item_info
    assert main_menu('q') == exit_program

    # This is my eureka moment on how to monkeypatch multiple inputs
    user_input = ['q', '2', '1']
    monkeypatch.setattr('builtins.input', lambda x: user_input.pop())

    assert main_menu() == add_new_item
    assert main_menu() == item_info
    assert main_menu() == exit_program


def test_get_price():
    """Tests that get_price returns the expected, bad value"""
    assert get_price(100) == 100
    assert get_price(1000) == 1000
    assert get_price(-100) == -100
    assert get_price(-1000) == -1000


# I'm not all together happy with this test, but it covers the code.
# Also, it took a lot of research to make this work with pytest over unittest.
def test_new_item_inventory(monkeypatch, mocker):
    """Tests adding a new item of type Inventory"""
    product_code = 100
    description = 'Chair'
    market_price = 388
    rental_price = 50
    user_input = ['n', 'n', rental_price, description, product_code]

    with captured_output() as out:
        mock_inventory = mocker.patch.object(Inventory, 'return_as_dictionary')
        mock_price = mocker.patch('inventory_management.market_prices.' +
                                  'get_latest_price', return_value=market_price)
        monkeypatch.setattr('builtins.input', lambda x: user_input.pop())

        add_new_item()

        mock_inventory.assert_called_once()
        mock_price.assert_called_once_with(product_code)

        output = out.getvalue()
    assert 'New inventory item added' in output
    assert product_code in FULL_INVENTORY

    print(FULL_INVENTORY)
    # assert False


def test_new_item_furniture(monkeypatch, mocker):
    """Tests adding a new item of type Furniture"""
    product_code = 100
    description = 'Chair'
    market_price = 388
    rental_price = 50
    material = 'Leather'
    size = 'L'
    user_input = [size, material, 'y', rental_price, description, product_code]

    with captured_output() as out:
        mock_furniture = mocker.patch.object(Furniture, 'return_as_dictionary')
        mock_price = mocker.patch('inventory_management.market_prices.' +
                                  'get_latest_price', return_value=market_price)
        monkeypatch.setattr('builtins.input', lambda x: user_input.pop())

        add_new_item()

        mock_furniture.assert_called_once()
        mock_price.assert_called_once_with(product_code)

        output = out.getvalue()
    assert 'New inventory item added' in output
    assert product_code in FULL_INVENTORY

    print(FULL_INVENTORY)
    # assert False


def test_new_item_electric_app(monkeypatch, mocker):
    """Tests adding a new item of type ElectricAppliances"""
    product_code = 100
    description = 'Oven'
    market_price = 388
    rental_price = 50
    brand = 'Samsung'
    voltage = '230'
    user_input = [voltage, brand, 'y', 'n',
                  rental_price, description, product_code]

    with captured_output() as out:
        mock_electric_appliances = \
            mocker.patch.object(ElectricAppliances, 'return_as_dictionary')
        mock_price = mocker.patch('inventory_management.market_prices.' +
                                  'get_latest_price', return_value=market_price)
        monkeypatch.setattr('builtins.input', lambda x: user_input.pop())

        add_new_item()

        mock_electric_appliances.assert_called_once()
        mock_price.assert_called_once_with(product_code)

        output = out.getvalue()
    assert 'New inventory item added' in output
    assert product_code in FULL_INVENTORY

    print(FULL_INVENTORY)
    # assert False


def test_item_info(monkeypatch):
    """Tests that item_info returns expected values"""
    expected_return = (f'product_code:100\n'
                       f'description:Chair\n'
                       f'market_price:100\n'
                       f'rental_price:20\n')
    FULL_INVENTORY['100'] = {'product_code': '100',
                             'description': 'Chair',
                             'market_price': '100',
                             'rental_price': '20'}

    monkeypatch.setattr('builtins.input', lambda x: '100')
    with captured_output() as out:
        item_info()
    output = out.getvalue()
    print(output)
    print(expected_return)
    assert output == expected_return

    monkeypatch.setattr('builtins.input', lambda x: '200')
    with captured_output() as out:
        item_info()
    output = out.getvalue()
    print(output)
    print(expected_return)
    assert output == 'Item not found in inventory\n'


def test_exit_program():
    """Tests that exit_program calls sys.exit() properly"""

    with pytest.raises(SystemExit):
        exit_program()


# ------------------- Inventory management module tests ------------------ #

def test_init_inventory():
    """Tests that inventory class initializes correctly"""
    product_dict = {}
    product_dict['product_code'] = 100
    product_dict['description'] = 'Chair'
    product_dict['market_price'] = 200
    product_dict['rental_price'] = 50

    inventory = Inventory(**product_dict)

    print(inventory.return_as_dictionary())
    print(product_dict)

    assert inventory.product_code == product_dict['product_code']
    assert inventory.description == product_dict['description']
    assert inventory.market_price == product_dict['market_price']
    assert inventory.rental_price == product_dict['rental_price']


def test_return_as_dict_inventory():
    """Tests that inventory class returns the expected dictionary"""
    product_dict = {}
    product_dict['product_code'] = 100
    product_dict['description'] = 'Chair'
    product_dict['market_price'] = 200
    product_dict['rental_price'] = 50

    inventory = Inventory(**product_dict)

    print(inventory.return_as_dictionary())
    print(product_dict)

    assert product_dict == inventory.return_as_dictionary()


def test_init_furniture():
    """Tests that furniture class initializes correctly"""
    product_dict = {}
    product_dict['product_code'] = 100
    product_dict['description'] = 'Chair'
    product_dict['market_price'] = 200
    product_dict['rental_price'] = 50
    product_dict['material'] = 'Leather'
    product_dict['size'] = 'L'

    chair = Furniture(**product_dict)

    print(chair.return_as_dictionary())
    print(product_dict)

    assert chair.product_code == product_dict['product_code']
    assert chair.description == product_dict['description']
    assert chair.market_price == product_dict['market_price']
    assert chair.rental_price == product_dict['rental_price']
    assert chair.material == product_dict['material']
    assert chair.size == product_dict['size']


def test_return_as_dict_furniture():
    """Tests that furniture class returns the expected dictionary"""
    product_dict = {}
    product_dict['product_code'] = 100
    product_dict['description'] = 'Chair'
    product_dict['market_price'] = 200
    product_dict['rental_price'] = 50
    product_dict['material'] = 'Leather'
    product_dict['size'] = 'L'

    chair = Furniture(**product_dict)

    print(chair.return_as_dictionary())
    print(product_dict)

    assert product_dict == chair.return_as_dictionary()


def test_init_appliance():
    """Tests that electric appliance class initializes correctly"""
    product_dict = {}
    product_dict['product_code'] = 8942
    product_dict['description'] = 'Oven'
    product_dict['market_price'] = 600
    product_dict['rental_price'] = 200
    product_dict['brand'] = 'Samsung'
    product_dict['voltage'] = 230

    oven = ElectricAppliances(**product_dict)

    print(oven.return_as_dictionary())
    print(product_dict)

    assert oven.product_code == product_dict['product_code']
    assert oven.description == product_dict['description']
    assert oven.market_price == product_dict['market_price']
    assert oven.rental_price == product_dict['rental_price']
    assert oven.brand == product_dict['brand']
    assert oven.voltage == product_dict['voltage']


def test_return_as_dict_appliance():
    """Tests that electric appliance class returns the expected dictionary"""
    product_dict = {}
    product_dict['product_code'] = 8942
    product_dict['description'] = 'Oven'
    product_dict['market_price'] = 600
    product_dict['rental_price'] = 200
    product_dict['brand'] = 'Samsung'
    product_dict['voltage'] = 230

    oven = ElectricAppliances(**product_dict)

    print(oven.return_as_dictionary())
    print(product_dict)

    assert product_dict == oven.return_as_dictionary()


def test_get_latest_price_market():
    """Tests that get latest price returns the expected value.

    In this case, the expected value is what we pass in.
    We're testing a broken output yielding incorrect results.

    """
    assert get_latest_price(100) == 100
    assert get_latest_price(1000) == 1000
    assert get_latest_price(-100) == -100
    assert get_latest_price(-1000) == -1000
