#!/usr/bin/env python3

import mock
import os
import platform
import unittest


from io import StringIO
from students.jeff_shabani.lesson01.assignment.inventory_management.electricappliancesclass import ElectricAppliances
from students.jeff_shabani.lesson01.assignment.inventory_management.furnitureclass import Furniture
from students.jeff_shabani.lesson01.assignment.inventory_management.inventoryclass import Inventory
from pathlib import Path
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

class TestInventoryManagement(unittest.TestCase):


    def setUp(self):
        self.appliance = ElectricAppliances(*APPLIANCE.values())
        self.furniture = Furniture(*CHAIR.values())
        self.inventory = Inventory(*GENERIC_INVETORY.values())

    def test_generic_inventory(self):
        """
        Test electric appliance dictionary output"""
        item = self.inventory
        expected = item.returnasdictionary()
        self.assertDictEqual(GENERIC_INVETORY, expected)

    def test_electric_appliance(self):
        """
        Test electric appliance dictionary output"""
        freezer = self.appliance
        expected = freezer.returnasdictionary()
        self.assertDictEqual(APPLIANCE, expected)

    def test_furniture(self):
        """
        Test furniture dictionary output"""
        recliner = self.furniture
        expected = recliner.returnasdictionary()
        self.assertDictEqual(CHAIR, expected)

    # def test_program_quit(self):
    #     """Test that the program quits properly"""
    #     d = mainmenu()
    #     with self.assertRaises(SystemExit):
    #         d.exitprogram()
    #     del d


    def tearDown(self):
        del self.appliance
        del self.furniture
        del self.inventory



