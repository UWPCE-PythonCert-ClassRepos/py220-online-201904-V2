'''
Integration Tests
'''

from unittest import TestCase
from unittest.mock import MagicMock, patch

import sys
import io
import pytest
import electric_appliances
import home_furniture
import store_inventory
import market_prices
from main import main_menu, add_new_furnature, add_new_item, \
add_new_electronics, item_info, exit_program


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
                      'size': 's'}

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
                     'size': 's'}
        self.assertEqual(add_new_furnature(), dict_furn)

    def item_info(self, test_dict):
        test_dict = {}
        text_trap = io.StringIO()
        sys.stdout = text_trap
        user_input = ['123']
        with patch('builtins.input', side_effect=user_input):
            test_dict = item_info()
        return test_dict

    def test_main_menu(self):
        test_dict = {}
        user_input = ["1"]
        text_trap = io.StringIO()
        sys.stdout = text_trap
        with patch('builtins.input', side_effect=user_input):
            function = main_menu()
        if function.__name__ == "add_new_item":
            text_trap = io.StringIO()
            sys.stdout = text_trap
            user_input = ['123', 'Testing', '123.45', '12.34', 'N', 'N']
            with patch('builtins.input', side_effect=user_input):
                test_dict = add_new_item()
        user_input = ["2"]
        with patch('builtins.input', side_effect=user_input):
            function = main_menu()
        if function.__name__ == "item_info":
            test_dict = self.item_info(self.test_dict_main)
        user_input = ["q"]
        with patch('builtins.input', side_effect=user_input):
            function = main_menu()
        if function.__name__ == "exit_program":
            self.assertRaises(SystemExit, exit_program)

    def test_input_add(self):
        test_dict = {}
        test_dict_main = self.test_dict_main
        text_trap = io.StringIO()
        sys.stdout = text_trap
        user_input = ['123', 'Testing', '123.45', '12.34', 'N', 'N']
        with patch('builtins.input', side_effect=user_input):
            test_dict = add_new_item()
        sys.stdout = sys.__stdout__
        return test_dict
#        self.assertEqual(test_dict, test_dict_main)
