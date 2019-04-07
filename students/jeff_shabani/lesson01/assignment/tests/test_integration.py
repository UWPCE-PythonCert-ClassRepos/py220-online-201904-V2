#!/usr/bin/env python3

"""
this function is necessary to change the working directory
to inventory management.
"""

from changedirectory import changedirectory

changedirectory()

from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest
import electricappliancesclass
import furnitureclass
import inventoryclass
import market_prices
from main import mainmenu


class MainMenuTests(TestCase):
    """
    Full test of inventory management main module. Tests
    user input and returned results.
    """

    inv_dict = {'product_code': '111',
                'description': 'Testing',
                'market_price': '100',
                'rental_price': '120'}

    appl_dict = {'product_code': '222',
                 'description': 'Espressmaschine',
                 'market_price': '2000',
                 'rental_price': '2200',
                 'brand': 'Gaggia',
                 'voltage': '64'}

    furniture_dict = {'product_code': '333',
                      'description': 'Recliner',
                      'market_price': '3000',
                      'rental_price': '3500',
                      'material': 'Leder',
                      'size': 'M'}

    @patch('main.addnewitem', return_value=inv_dict)
    def test_add_non_appliance_furniture(self, addnewitem):
        """
        Tests adding a new item that's neither
        furniture nor appliance.
        """

        inv_add = {'product_code': '111',
                   'description': 'Testing',
                   'market_price': '100',
                   'rental_price': '120'}
        self.assertEqual(addnewitem(), inv_add)

    @patch('main.add_appliance', return_value=appl_dict)
    def test_add_appliance(self, add_appliance):
        """
        Tests adding an appliance"""

        appl_add = {'product_code': '222',
                    'description': 'Espressmaschine',
                    'market_price': '2000',
                    'rental_price': '2200',
                    'brand': 'Gaggia',
                    'voltage': '64'}
        self.assertEqual(add_appliance(), appl_add)

    @patch('main.add_furniture', return_value=furniture_dict)
    def test_add_furniture(self, add_furniture):
        """
        Tests adding peice of furniture"""

        dict_furn = {'product_code': '333',
                     'description': 'Recliner',
                     'market_price': '3000',
                     'rental_price': '3500',
                     'material': 'Leder',
                     'size': 'M'}
        self.assertEqual(add_furniture(), dict_furn)

if __name__ == '__main__':
    unittest.main()
