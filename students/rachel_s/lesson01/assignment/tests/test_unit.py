#!/usr/bin/env python

"""Unit tests for each module in the inventory management package"""

import pytest
from unittest import TestCase
from unittest.mock import patch, MagicMock
from unittest import mock
from inventory import Inventory
from electric_appliances import ElectricAppliances
from furniture import Furniture
import market_prices
import main


class Inventory_Test(TestCase):
    """Tests for Inventory class"""

    def test_inventory(self):
        """Tests for Inventory dictionary output"""
        my_inv = Inventory(product_code=12, description='an apple',
                        market_price=2, rental_price=1.5)
        inv_dict = my_inv.return_as_dictionary()
        assert inv_dict['product_code'] == 12
        assert inv_dict['description'] == 'an apple'
        assert inv_dict['market_price'] == 2
        assert inv_dict['rental_price'] == 1.5


class ElectricAppliances_Test(TestCase):
    """Tests for ElectricAppliances class"""

    def test_electric_appliances(self):
        """Tests for ElectricAppliances dictionary output"""
        my_inv = ElectricAppliances(
            product_code=12, description='electric apple', market_price=7,
            rental_price=4.5, brand='fruitcorp', voltage=240)
        inv_dict = my_inv.return_as_dictionary()
        assert inv_dict['product_code'] == 12
        assert inv_dict['description'] == 'electric apple'
        assert inv_dict['market_price'] == 7
        assert inv_dict['rental_price'] == 4.5
        assert inv_dict['brand'] == 'fruitcorp'
        assert inv_dict['voltage'] == 240


class Furniture_Test(TestCase):
    """Tests for Furniture class"""
    def test_furniture(self):
        """Tests for Furniture dictionary output"""
        my_inv = Furniture(
            product_code=12, description='apple chair', market_price=70,
            rental_price=45, material='apple', size=12)
        inv_dict = my_inv.return_as_dictionary()
        assert inv_dict['product_code'] == 12
        assert inv_dict['description'] == 'apple chair'
        assert inv_dict['market_price'] == 70
        assert inv_dict['rental_price'] == 45
        assert inv_dict['material'] == 'apple'
        assert inv_dict['size'] == 12


class MarketPrices_Test(TestCase):
    """Tests market_prices"""

    def test_market_prices(self):
        """Tests get_latest_price output"""
        assert market_prices.get_latest_price(1) == 24


class Main_Test(TestCase):
    """Tests for main module"""

    def test_get_price(self):
        """Tests get_price method from main"""
        assert main.get_price(2) == "Get price for 2"
