#!/usr/bin/env python3
"""Unittest cases for integration testing"""

# Douglas Klos
# April 4th, 2019
# Python 220, Lesson 01
# test_integration.py

import unittest
from unittest import TestCase

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances

# Feels like integration tests are just rebuilding main
#   with predefined values and no user input.
# Validates that the modules work together though I suppose.
# Also 80 width linting does not improve readability
#   in a language that is all about readability.


class IntegrationTests(TestCase):
    """Integration tests for inventory_management

    Attributes:
        item_chair (dict) : dictionary for chair item
        item_microwave (dict) : dictionary for microwave electric appliance
        item_sofa (dict) : dictionary for sofa furniture
        full_inventory (dict) : dictionary database of above items
        inventory_string (str) : string containing all data in full_inventory

    """

    def setUp(self):
        self.item_chair = {}
        self.item_microwave = {}
        self.item_sofa = {}
        self.full_inventory = {}
        self.inventory_string = ''

        self.item_chair['product_code'] = 100
        self.item_chair['description'] = 'Chair'
        self.item_chair['market_price'] = 111
        self.item_chair['rental_price'] = 11
        self.full_inventory[self.item_chair['product_code']] = \
            Inventory(**self.item_chair).return_as_dictionary()

        self.item_microwave['product_code'] = 200
        self.item_microwave['description'] = 'Microwave'
        self.item_microwave['market_price'] = 222
        self.item_microwave['rental_price'] = 22
        self.item_microwave['brand'] = 'Samsung'
        self.item_microwave['voltage'] = 230
        self.full_inventory[self.item_microwave['product_code']] = \
            ElectricAppliances(**self.item_microwave).return_as_dictionary()

        self.item_sofa['product_code'] = 300
        self.item_sofa['description'] = 'Sofa'
        self.item_sofa['market_price'] = 333
        self.item_sofa['rental_price'] = 33
        self.item_sofa['material'] = 'Leather'
        self.item_sofa['size'] = 'XL'
        self.full_inventory[self.item_sofa['product_code']] = \
            Furniture(**self.item_sofa).return_as_dictionary()

        for item_code in self.full_inventory:
            for value in self.full_inventory[item_code].values():
                self.inventory_string += f'{value}'

    def test_integration_chair(self):
        """Integration test for chair inventory

        Verifies that all chair related data is present.

        """
        self.assertIn(str(self.item_chair['product_code']),
                      self.inventory_string)
        self.assertIn(str(self.item_chair['description']),
                      self.inventory_string)
        self.assertIn(str(self.item_chair['market_price']),
                      self.inventory_string)
        self.assertIn(str(self.item_chair['rental_price']),
                      self.inventory_string)

    def test_integration_microwave(self):
        """Integration test for microwave electrical applicance

        Verifies that all microwave related data is present.

        """
        self.assertIn(str(self.item_microwave['product_code']),
                      self.inventory_string)
        self.assertIn(str(self.item_microwave['description']),
                      self.inventory_string)
        self.assertIn(str(self.item_microwave['market_price']),
                      self.inventory_string)
        self.assertIn(str(self.item_microwave['rental_price']),
                      self.inventory_string)
        self.assertIn(str(self.item_microwave['brand']),
                      self.inventory_string)
        self.assertIn(str(self.item_microwave['voltage']),
                      self.inventory_string)

    def test_integration_sofa(self):
        """Integration test for sofa furniture

        Verifies that all sofa related data is present.

        """
        self.assertIn(str(self.item_sofa['product_code']),
                      self.inventory_string)
        self.assertIn(str(self.item_sofa['description']),
                      self.inventory_string)
        self.assertIn(str(self.item_sofa['market_price']),
                      self.inventory_string)
        self.assertIn(str(self.item_sofa['rental_price']),
                      self.inventory_string)
        self.assertIn(str(self.item_sofa['material']),
                      self.inventory_string)
        self.assertIn(str(self.item_sofa['size']),
                      self.inventory_string)

    def test_full_string(self):
        """Integration test

        We build up a string of all the values in the database
        then we go through each expected value and remove it.
        If there's nothing left at the end then we pass

        """
        self.inventory_string = self.inventory_string.replace(
            str(self.item_chair['product_code']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_chair['description']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_chair['market_price']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_chair['rental_price']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_microwave['product_code']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_microwave['description']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_microwave['market_price']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_microwave['rental_price']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_microwave['brand']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_microwave['voltage']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_sofa['product_code']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_sofa['description']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_sofa['market_price']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_sofa['rental_price']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_sofa['material']), '')
        self.inventory_string = self.inventory_string.replace(
            str(self.item_sofa['size']), '')

        self.assertEqual(self.inventory_string, '')


if __name__ == '__main__':

    unittest.main()
