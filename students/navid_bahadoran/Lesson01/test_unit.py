"""Unittest cases for inventory management package"""

# Navid Bahadoran
# April 14th, 2019
# Lesson 01
# test_unit.py
from unittest import TestCase
from unittest.mock import patch
import unittest.main

from inventory_management import inventory_class as ic
from inventory_management import furniture_class as fc
from inventory_management import electric_appliances_class as ec
from inventory_management import market_prices
from inventory_management.main import add_new_item
from inventory_management.main import main_menu
from inventory_management.main import add_new_item
from inventory_management.main import item_info
from inventory_management.main import get_price
from inventory_management.main import exit_program
from inventory_management.main import FULL_INVENTORY


class InventoryTest(TestCase):

    def setUp(self):
        """ initialize our test product for inventory class"""
        self.test_dict = dict()
        self.test_dict['product_code'] = 1
        self.test_dict['description'] = "test unit"
        self.test_dict['market_price'] = 24
        self.test_dict['rental_price'] = 123
        self.new_item = ic.Inventory(**self.test_dict)

    def test_init_inventory_class(self):
        """ test the constructor of inventory class"""
        self.assertEqual(self.test_dict['product_code'], self.new_item.product_code)
        self.assertEqual(self.test_dict['description'], self.new_item.description)
        self.assertEqual(self.test_dict['market_price'], self.new_item.market_price)
        self.assertEqual(self.test_dict['rental_price'], self.new_item.rental_price)

    def test_inventory_class_return_as_dictionary(self):
        """ test return dictionary of inventory class"""
        self.assertEqual(self.new_item.return_as_dictionary(), self.test_dict)


class FurnitureTest(TestCase):
    """ test furniture class"""

    def setUp(self):
        """ initialize our test product for furniture class"""
        self.test_dict = dict()
        self.test_dict['product_code'] = 1
        self.test_dict['description'] = "test unit"
        self.test_dict['market_price'] = 24
        self.test_dict['rental_price'] = 123
        self.test_dict['material'] = "wood"
        self.test_dict['size'] = "L"
        self.new_item = fc.Furniture(**self.test_dict)

    def test_init_furniture_class(self):
        """ test the constructor of Furniture class"""
        self.assertEqual(self.test_dict['product_code'], self.new_item.product_code)
        self.assertEqual(self.test_dict['description'], self.new_item.description)
        self.assertEqual(self.test_dict['market_price'], self.new_item.market_price)
        self.assertEqual(self.test_dict['rental_price'], self.new_item.rental_price)
        self.assertEqual(self.test_dict['material'], self.new_item.material)
        self.assertEqual(self.test_dict['size'], self.new_item.size)

    def test_furniture_class(self):
        """ test return dictionary of furniture class"""
        self.assertEqual(self.new_item.return_as_dictionary(), self.test_dict)


class ElectricApplianceTest(TestCase):
    """ test electric appliance class """

    def setUp(self):
        """ initialize our test product for electrical appliance class"""
        self.test_dict = dict()
        self.test_dict['product_code'] = 1
        self.test_dict['description'] = "test unit"
        self.test_dict['market_price'] = 24
        self.test_dict['rental_price'] = 123
        self.test_dict['brand'] = "Samsung"
        self.test_dict['voltage'] = 110
        self.new_item = ec.ElectricAppliances(**self.test_dict)

    def test_init_electric_appliance_class(self):
        """ test the constructor of electric appliance class"""
        self.assertEqual(self.test_dict['product_code'], self.new_item.product_code)
        self.assertEqual(self.test_dict['description'], self.new_item.description)
        self.assertEqual(self.test_dict['market_price'], self.new_item.market_price)
        self.assertEqual(self.test_dict['rental_price'], self.new_item.rental_price)
        self.assertEqual(self.test_dict['brand'], self.new_item.brand)
        self.assertEqual(self.test_dict['voltage'], self.new_item.voltage)

    def test_electric_appliance_class(self):
        self.assertEqual(self.new_item.return_as_dictionary(), self.test_dict)


class MarketPriceTest(TestCase):
    """ test the market price"""

    def test_market_price_get_latest_price(self):
        """ test the market price return expect value in this case expected value is 24"""
        self.assertEqual(market_prices.get_latest_price(10), 24)
        self.assertEqual(market_prices.get_latest_price(20), 24)
        self.assertIsNone(market_prices.get_latest_price())


class MainTest(TestCase):
    """ test the main module"""

    def test_main_menu(self):
        side_effects = ['1', '2', 'q']
        with patch('inventory_management.main.input', side_effect=side_effects):
            with patch('inventory_management.main.print') as mock_print:
                self.assertEqual(main_menu(), add_new_item)
                assert mock_print.call_count == 4
                mock_print.assert_called_with("q. Quit")
                self.assertEqual(main_menu(), item_info)
                self.assertEqual(main_menu(), exit_program)

    def test_get_price(self):
        with patch('inventory_management.market_prices.get_latest_price') as mock_market_price:
            with patch("inventory_management.main.print") as mock_print:
                get_price()
                mock_market_price.assert_called_once()
                mock_print.assert_called_once_with("Get price")

    def test_add_new_item_inventory(self):
        side_effects = [1, "test_item", 200, 'n', 'n']
        with patch('inventory_management.market_prices.get_latest_price', return_value=24) as mock_market_price:
            with patch('inventory_management.main.input', side_effect=side_effects):
                with patch('inventory_management.inventory_class.Inventory') as mock_inventory:
                    with patch("inventory_management.main.print") as mock_print:
                        add_new_item()
                        mock_market_price.assert_called_once_with(1)
                        mock_inventory.assert_called_once_with(1, "test_item", 24, 200)
                        mock_print.assert_called_once_with("New inventory item added")
                        self.assertIn(1, FULL_INVENTORY)

    def test_add_new_item_electric_appliance(self):
        side_effects = [1, "test_item", 200, 'n', 'y', 'Samsung', 110]
        with patch('inventory_management.market_prices.get_latest_price', return_value=24) as mock_market_price:
            with patch('inventory_management.main.input', side_effect=side_effects):
                with patch('inventory_management.electric_appliances_class.ElectricAppliances') as mock_electric:
                    with patch("inventory_management.main.print") as mock_print:
                        add_new_item()
                        mock_market_price.assert_called_once_with(1)
                        mock_electric.assert_called_once_with(1, "test_item", 24, 200, 'Samsung', 110)
                        mock_print.assert_called_once_with("New inventory item added")
                        self.assertIn(1, FULL_INVENTORY)

    def test_add_new_item_furniture(self):
        """ test add new item to check if adds new item to the full_inventory dict"""
        side_effects = [1, "test_item", 200, 'y', 'Wood', "L"]
        with patch('inventory_management.market_prices.get_latest_price', return_value=24) as mock_market_price:
            with patch('inventory_management.main.input', side_effect=side_effects):
                with patch('inventory_management.furniture_class.Furniture') as mock_furniture:
                    with patch("inventory_management.main.print") as mock_print:
                        add_new_item()
                        mock_market_price.assert_called_once_with(1)
                        mock_furniture.assert_called_once_with(1, "test_item", 24, 200, 'Wood', "L")
                        mock_print.assert_called_once_with("New inventory item added")
                        self.assertIn(1, FULL_INVENTORY)

    def test_item_info(self):
        """ test item_info function to check if it finds the inventory in the full_inventory dict"""
        full_inventory_dict = dict()
        full_inventory_dict['product_code'] = 1
        full_inventory_dict['description'] = "test unit"
        full_inventory_dict['market_price'] = 24
        full_inventory_dict['rental_price'] = 123
        with patch.dict("inventory_management.main.FULL_INVENTORY", {"1": full_inventory_dict}):
            with patch('inventory_management.main.input', side_effect=["1"]):
                with patch('inventory_management.main.print') as mock_print:
                    item_info()
                    mock_print.assert_called_with("rental_price:123")
        with patch.dict("inventory_management.main.FULL_INVENTORY", {"1": full_inventory_dict}):
            with patch('inventory_management.main.input', side_effect=["2"]):
                with patch('inventory_management.main.print') as mock_print:
                    item_info()
                    mock_print.assert_called_once_with("Item not found in inventory")

    def test_exit_program(self):
        """ test the exit_program function"""
        with patch("inventory_management.main.sys.exit") as mock_exit:
            exit_program()
            mock_exit.assert_called_once()
        with self.assertRaises(SystemExit):
            exit_program()


if __name__ == "__main__":
    unittest.main()
