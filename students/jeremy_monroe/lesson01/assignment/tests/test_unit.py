""" Unit tests for inventory management. """

import unittest
from unittest.mock import MagicMock

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
        """ Tests main.main_menu using simulated user input. """

        self.assertEqual(main.main_menu('1'), main.add_new_item)
        self.assertEqual(main.main_menu('2'), main.item_info)
        self.assertEqual(main.main_menu('q'), main.exit_program)

    def test_item_info(self):
        """ Tests main.add_new_item using simulated user input. """

        new_item = Furniture(5, 'Desk', 500, 50, 'wood', 'l')
        new_item_dict = new_item.return_as_dictionary()
        test_dict = {5: new_item_dict}

        main.item_info = MagicMock(return_value=test_dict[5]['description'])

        self.assertEqual('Desk', main.item_info())

    def test_system_exit(self):
        """ Tests main.exit_program. """

        with self.assertRaises(SystemExit):
            main.exit_program()
