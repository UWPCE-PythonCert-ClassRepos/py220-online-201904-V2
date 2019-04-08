""" Unit tests for inventory management. """

import unittest
import io
import sys
from unittest.mock import MagicMock, patch

from inventory_class import Inventory
from furniture_class import Furniture
from electric_appliances_class import ElectricAppliances
import main
import market_prices


class InventoryClassTests(unittest.TestCase):
    """ Tests for inventory_class module. """

    def test_inventory_initialization(self):
        """ Tests for successful, accurate initalization of Inventory. """

        new_product = Inventory(1, 'Chair', 100, 20)
        new_product_dict = new_product.return_as_dictionary()

        self.assertEqual(1, new_product_dict['product_code'])
        self.assertEqual('Chair', new_product_dict['description'])
        self.assertEqual(100, new_product_dict['market_price'])
        self.assertEqual(20, new_product_dict['rental_price'])


class FurnitureClasstests(unittest.TestCase):
    """ Tests for furniture_class module. """

    def test_furniture_initalization(self):
        """ Test for succesful, accurate initialization of Furniture. """

        new_product = Furniture(2, 'Sofa', 600, 175, 'leather', 'l')
        new_product_dict = new_product.return_as_dictionary()

        self.assertEqual(2, new_product_dict['product_code'])
        self.assertEqual('Sofa', new_product_dict['description'])
        self.assertEqual(600, new_product_dict['market_price'])
        self.assertEqual(175, new_product_dict['rental_price'])
        self.assertEqual('leather', new_product_dict['material'])
        self.assertEqual('l', new_product_dict['size'])


class ElectricAppliancesTests(unittest.TestCase):
    """ Tests for electric_appliances_class module. """

    def test_electric_appliances_initialization(self):
        """
        Tests for successful, accurate initalization of ElectricAppliances.
        """

        new_product = ElectricAppliances(3, 'Blender', 200, 20, 'Krups', 110)
        new_product_dict = new_product.return_as_dictionary()

        self.assertEqual(3, new_product_dict['product_code'])
        self.assertEqual('Blender', new_product_dict['description'])
        self.assertEqual(200, new_product_dict['market_price'])
        self.assertEqual(20, new_product_dict['rental_price'])
        self.assertEqual('Krups', new_product_dict['brand'])
        self.assertEqual(110, new_product_dict['voltage'])


class MarketPricesTests(unittest.TestCase):
    """ Tests for market_prices module. """

    def test_get_latest_price(self):
        """
        Test to ensure get_latest_price is called with expected argument.
        """

        self.assertEqual(100, market_prices.get_latest_price(100))

        market_prices.get_latest_price = MagicMock(return_value=24)
        market_prices.get_latest_price(100)

        market_prices.get_latest_price.assert_called_with(100)


class MainTests(unittest.TestCase):
    """ Tests for the main module. """

    def test_main_menu(self):
        """ 
        Tests main.main_menu in a couple different ways.

        First by passing in a menu option as an argument.
        And second by using simulated user input to navigate the menu.

        Both tests verify that the proper function is called based on the menu
        input provided.
        """

        self.assertEqual(main.main_menu('1'), main.add_new_item)
        self.assertEqual(main.main_menu('2'), main.item_info)
        self.assertEqual(main.main_menu('q'), main.exit_program)

        inputs = (user_in for user_in in ['What?', '1'])
        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', mock_input):
            main_menu_output = main.main_menu()

        self.assertEqual(main.add_new_item, main_menu_output)


        inputs2 = (user_in2 for user_in2 in ['Yes', 'NO', '2'])
        def mock_input2(prompt):
            return next(inputs2)

        with patch('builtins.input', mock_input2):
            main_menu_output2 = main.main_menu()

        self.assertEqual(main.item_info, main_menu_output2)

    def test_get_price(self):
        """
        Calls main.get_price and verifies the content of its print statement.
        """
        expected_output = "Get price\n"

        captured_output = io.StringIO()
        sys.stdout = captured_output

        main.get_price()
        sys.stdout = sys.__stdout__

        self.assertEqual(expected_output, captured_output.getvalue())

    def test_add_new_item(self):
        """ Tests main.add_new_item with simulated user input. """

        main.FULL_INVENTORY = {}

        inputs = (user_in for user_in in [999, 'Vase', 1400, 'n', 'n'])

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', mock_input):
            main.add_new_item()

        test_dict = {'product_code': 999, 'description': 'Vase', 'market_price': 24,
                     'rental_price': 1400}

        self.assertEqual(test_dict, main.FULL_INVENTORY[999])

    def test_add_new_item_furniture(self):
        """
        Tests main.add_new_item with simulated user input by populating
        FULL_INVENTORY with a sample product and verifying that product is stored
        with the expected keys and values.
        """

        main.FULL_INVENTORY = {}

        inputs = (user_in for user_in in [123, 'Desk', 125, 'y', 'wood', 'l'])

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', mock_input):
            main.add_new_item()

        test_dict = {'product_code': 123, 'description': 'Desk', 'market_price': 24,
                     'rental_price': 125, 'material': 'wood', 'size': 'l'}

        self.assertEqual(test_dict, main.FULL_INVENTORY[123])

    def test_add_new_item_electric_appliance(self):
        """ Tests main.add_new_item with simulated user input. """

        main.FULL_INVENTORY = {}

        inputs = (user_in for user_in in [
                  246, 'Blender', 75, 'n', 'y', 'Krups', 110])

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', mock_input):
            main.add_new_item()

        test_dict = {'product_code': 246, 'description': 'Blender', 'market_price': 24,
                     'rental_price': 75, 'brand': 'Krups', 'voltage': 110}

        self.assertEqual(test_dict, main.FULL_INVENTORY[246])

    def test_item_info(self):
        """ 
        Testing main.item_info by adding an item to FULL_INVENTORY, calling
        item_info with its item_code, and capturing item_info's print statements
        to verify their accuracy.
        """

        main.FULL_INVENTORY = {}
        inputs = (user_in for user_in in [999, 'Vase', 1400, 'n', 'n'])

        def mock_input(prompt):
            return next(inputs)

        with patch('builtins.input', mock_input):
            main.add_new_item()

        expected_output = ('product_code:999\n'
                           'description:Vase\n'
                           'market_price:24\n'
                           'rental_price:1400\n')

        expected_output2 = "Item not found in inventory\n"

        captured_output = io.StringIO()
        sys.stdout = captured_output

        main.item_info(999)
        sys.stdout = sys.__stdout__

        self.assertEqual(expected_output, captured_output.getvalue())

        captured_output2 = io.StringIO()
        sys.stdout = captured_output2

        main.item_info(432)
        sys.stdout = sys.__stdout__

        self.assertEqual(expected_output2, captured_output2.getvalue())

    def test_system_exit(self):
        """ Tests main.exit_program. """

        with self.assertRaises(SystemExit):
            main.exit_program()
