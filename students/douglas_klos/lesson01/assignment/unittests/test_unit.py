#!/usr/bin/env python3
"""Unittest cases for inventory management module and main"""

# Douglas Klos
# April 4th, 2019
# Python 220, Lesson 01
# test_unit.py

import sys
import unittest
from unittest import TestCase
from unittest.mock import patch
from contextlib import contextmanager
from io import StringIO

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


class MainTests(TestCase):
    """Test cases for main.py"""

    def test_main_menu(self):
        """Tests that main_menu accepts user input
        and returns corrent function calls

        """
        self.assertEqual(main_menu('1'), add_new_item)
        self.assertEqual(main_menu('2'), item_info)
        self.assertEqual(main_menu('q'), exit_program)

        side_effects = ['1', '2', 'q']
        with patch('builtins.input', side_effect=side_effects):
            self.assertEqual(main_menu(), add_new_item)
            self.assertEqual(main_menu(), item_info)
            self.assertEqual(main_menu(), exit_program)

    def test_get_price(self):
        """Tests that get_price returns the expected, bad value"""
        self.assertEqual(get_price(100), 100)
        self.assertEqual(get_price(1000), 1000)
        self.assertEqual(get_price(-100), -100)
        self.assertEqual(get_price(-1000), -1000)

    # We were getting too many nested patch statements for 80 char
    #   So we're implementing some of the patching with decorators.
    @patch('inventory_management.' +
           'market_prices.get_latest_price', return_value=388)
    @patch('inventory_management.inventory_class.Inventory')
    def test_new_item_inventory(self, mock_inventory, mock_price):
        """Tests adding a new item of type Inventory"""
        product_code = 100
        description = 'Chair'
        market_price = 388
        rental_price = 50
        user_input = [product_code, description, rental_price, 'n', 'n']

        with captured_output() as out:
            with patch('builtins.input', side_effect=user_input):

                add_new_item()
                mock_price.assert_called_once_with(product_code)
                mock_inventory.assert_called_once_with(product_code,
                                                       description,
                                                       market_price,
                                                       rental_price)
                output = out.getvalue()
                self.assertIn("New inventory item added", output)
                self.assertIn(product_code, FULL_INVENTORY)

    @patch('inventory_management.' +
           'market_prices.get_latest_price', return_value=388)
    @patch('inventory_management.furniture_class.Furniture')
    def test_new_item_furniture(self, mock_furniture, mock_price):
        """Tests adding a new item of type Furniture"""
        product_code = 100
        description = 'Chair'
        market_price = 388
        rental_price = 50
        material = 'Leather'
        size = 'L'
        user_input = [product_code, description, rental_price,
                      'y', material, size]

        with captured_output() as out:
            with patch('builtins.input', side_effect=user_input):
                add_new_item()
                mock_price.assert_called_once_with(product_code)
                mock_furniture.assert_called_once_with(product_code,
                                                       description,
                                                       market_price,
                                                       rental_price,
                                                       material,
                                                       size)
                output = out.getvalue()
                self.assertIn("New inventory item added", output)
                self.assertIn(product_code, FULL_INVENTORY)

    @patch('inventory_management.' +
           'market_prices.get_latest_price', return_value=388)
    @patch('inventory_management.electric_appliances_class.ElectricAppliances')
    def test_new_item_electric_app(self, mock_elec_app, mock_price):
        """Tests adding a new item of type ElectricAppliance"""
        product_code = 100
        description = 'Oven'
        market_price = 388
        rental_price = 50
        brand = 'Samsung'
        voltage = 230
        user_input = [product_code, description, rental_price,
                      'n', 'y', brand, voltage]

        with captured_output() as out:
            with patch('builtins.input', side_effect=user_input):
                add_new_item()
                mock_price.assert_called_once_with(product_code)
                mock_elec_app.assert_called_once_with(product_code,
                                                      description,
                                                      market_price,
                                                      rental_price,
                                                      brand,
                                                      voltage)
                output = out.getvalue()
                self.assertIn("New inventory item added", output)
                self.assertIn(product_code, FULL_INVENTORY)

    def test_item_info(self):
        """Tests that item_info returns expected values"""
        expected_return = (f'product_code:100\n'
                           f'description:Chair\n'
                           f'market_price:100\n'
                           f'rental_price:20\n')
        FULL_INVENTORY['100'] = {'product_code': '100',
                                 'description': 'Chair',
                                 'market_price': '100',
                                 'rental_price': '20'}

        user_input = ['100']
        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                item_info()
        output = out.getvalue()
        self.assertEqual(output, expected_return)

        user_input = ['200']
        with patch('builtins.input', side_effect=user_input):
            with captured_output() as out:
                item_info()
        output = out.getvalue()
        self.assertEqual(output, 'Item not found in inventory\n')

    def test_exit_program(self):
        """Tests that exit_program calls sys.exit() properly"""
        with self.assertRaises(SystemExit):
            exit_program()


class InventoryTests(TestCase):
    """Test cases for Inventory class"""

    def setUp(self):
        self.product_dict = {}
        self.product_dict['product_code'] = 100
        self.product_dict['description'] = 'Chair'
        self.product_dict['market_price'] = 200
        self.product_dict['rental_price'] = 50
        self.inventory = Inventory(**self.product_dict)

    def test_init(self):
        """Tests that inventory class initializes correctly"""
        self.assertEqual(self.inventory.product_code,
                         self.product_dict['product_code'])
        self.assertEqual(self.inventory.description,
                         self.product_dict['description'])
        self.assertEqual(self.inventory.market_price,
                         self.product_dict['market_price'])
        self.assertEqual(self.inventory.rental_price,
                         self.product_dict['rental_price'])

    def test_return_as_dictionary(self):
        """Tests that inventory class returns the expected dictionary"""
        self.assertEqual(self.product_dict,
                         self.inventory.return_as_dictionary())


class FurnitureTests(TestCase):
    """Test cases for Furniture class"""

    def setUp(self):
        self.product_dict = {}
        self.product_dict['product_code'] = 100
        self.product_dict['description'] = 'Chair'
        self.product_dict['market_price'] = 200
        self.product_dict['rental_price'] = 50
        self.product_dict['material'] = 'Leather'
        self.product_dict['size'] = 'L'
        self.chair = Furniture(**self.product_dict)

    def test_init(self):
        """Tests that furniture class initializes correctly"""
        self.assertEqual(self.chair.product_code,
                         self.product_dict['product_code'])
        self.assertEqual(self.chair.description,
                         self.product_dict['description'])
        self.assertEqual(self.chair.market_price,
                         self.product_dict['market_price'])
        self.assertEqual(self.chair.rental_price,
                         self.product_dict['rental_price'])
        self.assertEqual(self.chair.material,
                         self.product_dict['material'])
        self.assertEqual(self.chair.size,
                         self.product_dict['size'])

    def test_return_as_dictionary(self):
        """Tests that furniture class returns the expected dictionary"""
        self.assertEqual(self.product_dict, self.chair.return_as_dictionary())


class ApplianceTest(TestCase):
    """Test cases for Electric Appliance class"""

    def setUp(self):
        self.product_dict = {}
        self.product_dict['product_code'] = 8942
        self.product_dict['description'] = 'Oven'
        self.product_dict['market_price'] = 600
        self.product_dict['rental_price'] = 200
        self.product_dict['brand'] = 'Samsung'
        self.product_dict['voltage'] = 230
        self.oven = ElectricAppliances(**self.product_dict)

    def test_init(self):
        """Tests that electric appliance class initializes correctly"""
        self.assertEqual(self.oven.product_code,
                         self.product_dict['product_code'])
        self.assertEqual(self.oven.description,
                         self.product_dict['description'])
        self.assertEqual(self.oven.market_price,
                         self.product_dict['market_price'])
        self.assertEqual(self.oven.rental_price,
                         self.product_dict['rental_price'])
        self.assertEqual(self.oven.brand,
                         self.product_dict['brand'])
        self.assertEqual(self.oven.voltage,
                         self.product_dict['voltage'])

    def test_return_as_dictionary(self):
        """Tests that electric appliance returns the expected dictionary"""
        self.assertEqual(self.product_dict, self.oven.return_as_dictionary())


class MarketPricesTest(TestCase):
    """Test case for market_price.get_latest_price"""

    def test_get_latest_price(self):
        """Tests that get latest price returns the expected value.
        In this case, the expected value is what we pass in.
        The function is very broken.

        """
        self.assertEqual(get_latest_price(100), 100)
        self.assertEqual(get_latest_price(1000), 1000)
        self.assertEqual(get_latest_price(-100), -100)
        self.assertEqual(get_latest_price(-1000), -1000)


if __name__ == '__main__':
    unittest.main()
