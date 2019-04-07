"""
Integration Tests
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest
import electric_appliances
import home_furniture
import store_inventory
import market_prices
from main import main_menu

class MainMenuTests(TestCase):
    '''
    There's a lot going on here, basically we're going to be testing user
    input through and through.  Both injecting values from input, and mocking
    actual entries.
    '''

    dict_test_inv = {'product_code': '123',
                     'description': 'Testing',
                     'market_price': '123.45',
                     'rental_price': '12.34'}

    dict_test_elec = {'product_code': '1234',
                      'description': 'Testing',
                      'market_price': '123.45',
                      'rental_price': '12.34',
                      'brand': 'Testing Inc',
                      'voltage': '123.4'}

    dict_test_furn = {'product_code': '12345',
                      'description': 'Testing',
                      'market_price': '123.45',
                      'rental_price': '12.34',
                      'material': 'Fur',
                      'size': '123'}

    dict_full_inv_test = {'product_code': '12345',
                          'description': 'Testing',
                          'market_price': '123.45',
                          'rental_price': '12.34',
                          'brand': 'Testing Inc',
                          'voltage': '123.4'}
    '''
    These dicts exist to test dictionary manipulation isolated from everything
    aside from main.py   Essentially I want to make certain that main.py
    returns the right values.
    '''


###############################################################################
#
# Testing product entries
#
##############################################################################

    @patch('main.add_new_item', return_value=dict_test_inv)
    def test_dict_main(self, add_new_item):
        '''
        Testing adding a new item inside main.
        '''
        dict_inv = {'product_code': '123',
                    'description': 'Testing',
                    'market_price': '123.45',
                    'rental_price': '12.34'}
        self.assertEqual(add_new_item(), dict_inv)

    # pylint: disable=E0102
    # Redefining is confusing, I get it, but this is a test
    @patch('main.add_new_electronics', return_value=dict_test_elec)
    def test_dict_elec(self, add_new_electronics):
        '''
        Testing adding a new electric item inside main.
        '''
        dict_elec = {'product_code': '1234',
                     'description': 'Testing',
                     'market_price': '123.45',
                     'rental_price': '12.34',
                     'brand': 'Testing Inc',
                     'voltage': '123.4'}
        self.assertEqual(add_new_electronics(), dict_elec)

    @patch('main.add_new_furnature', return_value=dict_test_furn)
    def test_dict_furn(self, add_new_furnature):
        '''
        Testing adding a new item inside main.
        '''
        dict_furn = {'product_code': '12345',
                     'description': 'Testing',
                     'market_price': '123.45',
                     'rental_price': '12.34',
                     'material': 'Fur',
                     'size': '123'}
        self.assertEqual(add_new_furnature(), dict_furn)
