#!/usr/bin/env python3

"""
this function is necessary to change the working directory
to inventory management.
"""
from changedirectory import changedirectory

changedirectory()

import os
import mock
import platform
import unittest

from pathlib import Path
from io import StringIO

import main
from main import addnewitem, ElectricAppliances, Furniture, Inventory, \
    mainmenu, exitprogram, get_latest_price, main_menu_for_testing

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

APPLIANCE = {'productcode': 'F100',
             'description': 'Freezer',
             'marketprice': 300,
             'rentalprice': 400,
             'brand': 'GE',
             'voltage': 200}

CHAIR = {'productcode': 'C100',
         'description': 'Recliner',
         'marketprice': 900,
         'rentalprice': 1200,
         'material': 'leather',
         'size': 'large'}

GENERIC_INVETORY = {'productcode': 'AAAA',
                    'description': 'Object',
                    'marketprice': 1,
                    'rentalprice': 2}

"""The dictionarires above are used to test the functionality
of the inventory management modules"""


class TestElectricAppliance(TestCase):
    def test_electric_appliance(self):
        """
        Test electric appliance dictionary output"""
        freezer = ElectricAppliances(*APPLIANCE.values())
        expected = freezer.returnasdictionary()
        self.assertDictEqual(APPLIANCE, expected)


class FurnitureTests(TestCase):
    def test_furniture(self):
        """
        Test furniture dictionary output"""
        recliner = Furniture(*CHAIR.values())
        expected = recliner.returnasdictionary()
        self.assertDictEqual(CHAIR, expected)


class InventoryTests(TestCase):
    def test_generic_inventory(self):
        """
        Test electric appliance dictionary output"""
        item = Inventory(*GENERIC_INVETORY.values())
        expected = item.returnasdictionary()
        self.assertDictEqual(GENERIC_INVETORY, expected)


class MarketPricesTests(TestCase):
    def test_get_market_price(self):
        """Test that get market price returns 24"""
        self.assertEqual(24, get_latest_price('placeholder'))


class MenuTests(TestCase):

    def test_main_menu_display(self):
        """Test console output main menu"""
        options_str = '({options_str})'
        expected = f'Please choose from the following options {options_str}:\n' \
            f'1. Add a new item to the inventory\n2. Get item ' \
            f'information\nq. Quit'
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            main_menu_for_testing()
            self.assertEqual(mocked_output.getvalue().strip(), expected)

    def test_main_menu_add_new(self):
        """
        Tests for menu item 1 selection"""
        while True:
            try:
                with patch('builtins.input', side_effect='1'):
                    self.assertEqual(mainmenu(), main.addnewitem())
            except StopIteration as error:
                return error

    def test_main_get_item_info(self):
        """
        Tests for item menu 2 selection"""
        while True:
            try:
                with patch('builtins.input', side_effect='2'):
                    self.assertEqual(mainmenu(), main.addnewitem())
            except StopIteration as error:
                return error

    @mock.patch('builtins.input', mock.Mock(return_value='q'))
    def test_program_quit(self):
        """
        Test that the program quits properly"""
        with self.assertRaises(SystemExit):
            main.exitprogram()


if __name__ == '__main__':
    unittest.main()
