"""Integration test cases for inventory management package"""

# Navid Bahadoran
# April 14th, 2019
# Lesson 01
# test_integration.py
from unittest import TestCase
import unittest.main

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management import market_prices
from inventory_management.main import add_new_item
from inventory_management.main import main_menu
from inventory_management.main import add_new_item
from inventory_management.main import item_info
from inventory_management.main import get_price
from inventory_management.main import exit_program
from inventory_management.main import FULL_INVENTORY


class IntegrationTests(TestCase):
    """Integration tests for inventory_management"""

    def setUp(self):
        self.item_table = dict()
        self.item_vacuum = dict()
        self.item_bed = dict()
        self.full_inventory = dict()

        self.item_table['product_code'] = 1
        self.item_table['description'] = 'Table'
        self.item_table['market_price'] = 24
        self.item_table['rental_price'] = 100
        self.full_inventory[self.item_table['product_code']] = \
            Inventory(**self.item_table).return_as_dictionary()

        self.item_vacuum['product_code'] = 2
        self.item_vacuum['description'] = 'Vacuum'
        self.item_vacuum['market_price'] = 24
        self.item_vacuum['rental_price'] = 200
        self.item_vacuum['brand'] = 'Samsung'
        self.item_vacuum['voltage'] = 110
        self.full_inventory[self.item_vacuum['product_code']] = \
            ElectricAppliances(**self.item_vacuum).return_as_dictionary()

        self.item_bed['product_code'] = 300
        self.item_bed['description'] = 'Bed'
        self.item_bed['market_price'] = 24
        self.item_bed['rental_price'] = 300
        self.item_bed['material'] = 'Wood'
        self.item_bed['size'] = 'L'
        self.full_inventory[self.item_bed['product_code']] = \
            Furniture(**self.item_bed).return_as_dictionary()

    def test_integration_table(self):
        """Integration test for table inventory"""
        self.assertEqual(self.full_inventory[self.item_table['product_code']], self.item_table)

    def test_integration_vacuum(self):
        """Integration test for vacuum"""
        self.assertEqual(self.full_inventory[self.item_vacuum['product_code']], self.item_vacuum)

    def test_integration_sofa(self):
        """Integration test for bed furniture"""
        self.assertEqual(self.full_inventory[self.item_bed['product_code']], self.item_bed)


if __name__ == "__main__":
    unittest.main()
