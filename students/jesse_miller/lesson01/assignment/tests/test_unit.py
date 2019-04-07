#!/usr/bin/env python3
'''
Testing methods for first lesson in Python220
'''
# import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock
from unittest import mock
import pytest
import main
import electric_appliances
import home_furniture
import store_inventory
import market_prices
from main import main_menu
# sys.path.append('/Users/jmiller/School/Python_220/students/jesse_miller/\
#                lesson01/assignment/')

'''
I tried just importing the directory, but no love.
'''

###############################################################################
#
# Starting with electric_appliances.py
#
###############################################################################


class ElectricAppliancesTest(TestCase):
    '''
    Testing electric_appliances addition to dict.
    '''

    def test_electric_dict(self):
        '''
        In this we will be making sure that output_dict functions correctly for
        inventory queries.  We do this by injecting dict input and then
        asserting that it exists when queried.
        '''
        electric_test = electric_appliances. \
            ElectricAppliances('12345', 'Testing', '123.45', '12.34',
                               'Testing Inc', '123.4')
        electric_dict_test = electric_test.return_as_dict()
        self.assertEqual(electric_dict_test, {'product_code': '12345',
                                              'description': 'Testing',
                                              'market_price': '123.45',
                                              'rental_price': '12.34',
                                              'brand': 'Testing Inc',
                                              'voltage': '123.4'})

###############################################################################
#
# Moving to home_furniture.py
#
###############################################################################


class HomeFurnatureTests(TestCase):
    '''
    Testing electric_appliances addition to dict.
    '''

    def test_furnature_dict(self):
        '''
        In this we will be making sure that output_dict functions correctly for
        inventory queries.  We do this by injecting dict input and then
        asserting that it exists when queried.  As above.
        '''
        furnature_test = home_furniture. \
            FurnitureClass('12345', 'Testing', '123.45', '12.34',
                           'Fur', '123')
        furnature_dict_test = furnature_test.return_as_dict()
        self.assertEqual(furnature_dict_test, {'product_code': '12345',
                                               'description': 'Testing',
                                               'market_price': '123.45',
                                               'rental_price': '12.34',
                                               'material': 'Fur',
                                               'size': '123'})


###############################################################################
#
# And now, store_inventory.py
#
###############################################################################


class InventoryTests(TestCase):
    '''
    Testing store_inventory.py
    '''

    def test_inventory_dict(self):
        '''
        In this we will be making sure that output_dict functions correctly for
        inventory queries.  We do this by injecting dict input and then
        asserting that it exists when queried.  As above.
        '''
        inventory_test = store_inventory. \
            Inventory('12345', 'Testing', '123.45', '12.34')
        furnature_dict_test = inventory_test.return_as_dict()
        self.assertEqual(furnature_dict_test, {'product_code': '12345',
                                               'description': 'Testing',
                                               'market_price': '123.45',
                                               'rental_price': '12.34'})


###############################################################################
#
# I guess we can test market_prices, but I'm not sure of the point since it
# just returns '24' no matter what.
#
###############################################################################


class MarketPricesTests(TestCase):
    '''
    So, this will be easy.  Basically just asserting that it's '24' and not
    anything else.
    '''

    def test_market_price(self):
        '''
        As stated above.  I'm injecting a value that I know will be overwritten
        by '24'
        '''
        prices = market_prices.get_latest_price('123')
        self.assertEqual(prices, 24)


###############################################################################
#
# So, here's where it'll get complicated.  The main_menu tests are going to be
# the brunt of the testing since that's where all the interaction is.  I've
# never been to clear on input testing, but here goes.
#
###############################################################################

    def test_menu_add(self):
        '''
        Here we test injecting a value of 1 in the menu
        '''
        while True:
            try:
                with patch('builtins.input', side_effect='1'):
                    self.assertEqual(main_menu(), main.add_new_item())
            except StopIteration as error_code:
                return error_code

    def test_menu_info(self):
        '''
        Testing number 2
        '''
        while True:
            try:
                with patch('builtins.input', side_effect='2'):
                    self.assertEqual(main_menu(), main.item_info())
            except StopIteration as error_code:
                return error_code

    def test_menu_quit(self):
        '''
        Testing q
        '''
        # while True:
            # try:
                # with patch('builtins.input', side_effect='q'):
                    # self.assertEqual(main_menu(), main.exit_program())
            # except StopIteration as error_code:
                # return error_code

        with mock.patch('builtins.input', return_value='q'):
            self.assertEqual(main_menu(), main.exit_program)

        # Why does this work but not the other...


###############################################################################
#
# Testing ancillary functions
#
###############################################################################


    def test_exit(self):
        '''
        Testing the exit function for clean exiting of program.
        '''
        with self.assertRaises(SystemExit):
            main.exit_program()

    def test_get_latest_price(self):
        '''
        Testing pricing return
        '''
        # pylint: disable=W0201
        self.get_price = MagicMock(return_value=24)
        self.assertEqual(24, main.get_price(1))
