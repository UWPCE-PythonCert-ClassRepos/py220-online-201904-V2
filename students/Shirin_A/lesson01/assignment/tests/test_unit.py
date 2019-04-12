"""Unit Test Module"""
# pylint: disable=C0303
from unittest.mock import patch
from unittest import TestCase
import sys
import pytest
sys.path.append(r"C:\Users\Public\py220-online-201904-V2\students\Shirin_A\lesson01\assignment\inventory_management")
from main import add_new_item, return_inventory
import main
from main import item_info, exit_program
#from electric_appliances import ElectricAppliances 
#from furniture_class import Furniture  
#from inventory_class import Inventory 
import market_prices

class ElectricAppliancesTest(TestCase):    
    """Testing Electric Appliances"""
    def test_electric_appliances(self):
        """ tests electric appliances class to return information about
            electric appliances in the inventory class as a dict"""
        testdict = {'productcode': '34',
                    'description': 'Toaster',
                    'marketprice': '24',
                    'rentalprice': '15',
                    'brand': 'frizi',
                    'voltage': '220'}
        electric_test = ElectricAppliances(*testdict.values())
        electric_dict_test = electric_test.return_as_dictionary()
        self.assertDictEqual(testdict, electric_dict_test)

class FurnitureClassTest(TestCase):
    """Testing Electric Appliances"""        
    def test_furniture(self):
        """ tests furniture class to return information about
            furniture items in the inventory class as a dict"""
        testdict = {'productcode': '340',
                    'description': 'chair',
                    'marketprice': '50',
                    'rentalprice': '60',
                    'material': 'wood',
                    'size': 'M'}
        furniture_test = furniture_class.Furniture(*testdict.values())
        furniture_dict_test = furniture_test.return_as_dictionary()
        self.assertDictEqual(testdict, furniture_dict_test)

class InventoryClassTest(TestCase):
    """Testing Electric Appliances"""        
    def test_inventory(self):
        """ tests inventory class returning a dict of all
            information about an item in the inventory"""
        testdict = {'productcode': '5',
                    'description': 'shoe',
                    'marketprice': '15',
                    'rentalprice': '20',}
        inventory_test = inventory_class.Inventory(*testdict.values())
        inventory_dict_test = inventory_test.return_as_dictionary()
        self.assertDictEqual(testdict, inventory_dict_test)        

class MarketPricesTest(TestCase):
    """testing market price"""    
    def test_market_price(self):
        """ Testing that it returns 24"""
        prices = market_prices.get_latest_price('550')
        self.assertEqual(prices, 24)

class MainMenuTests(TestCase):
    """
    This class tests the methods in the Main module
    """
    @patch('main.main_menu', return_value=add_new_item)
    def test_main_menu__add_item(self, main_menu):
        """tests that in main menu function, user input of
           1 will return add_new_item  """
        self.assertEqual(main_menu(1), add_new_item)

    @patch('main.main_menu', return_value=item_info)
    def test_main_menu_item_info(self, main_menu):
        """tests that in main menu function, user input of
           2 will return item_info"""
        self.assertEqual(main_menu(2), item_info)

    @patch('main.main_menu', return_value=exit_program)
    def test_main_manu_exit_program(self, main_menu):
        """tests that in main menu function, user input of
           3 will return exit_program """
        self.assertEqual(main_menu('q'), exit_program)


    def test_add_new_item(self):
        """Tests that each type of item (Furniture, Electric, Regular) gets
        added to inventory"""

        input1 = [1, 'shoes', 10, 'n', 'n']
        test_inventory = {1: {'productcode': 1, 'description': 'shoes',

                              'marketprice': 24, 'rentalprice': 10}}

        with patch('builtins.input', side_effect=input1):
            add_new_item()

        self.assertEqual(test_inventory, return_inventory())

        #add electric appliance to inventory

        input2 = [2, 'Toaster', 10, 'n', 'y', 'sony', 120]

        test_inventory = {1: {'productcode': 1, 'description': 'shoes',

                              'marketprice': 24, 'rentalprice': 10},

                          2: {'productcode': 2, 'description': 'Toaster',

                              'marketprice': 24, 'rentalprice': 10,
                              'brand': 'sony',
                              'voltage': 120}}

        with patch('builtins.input', side_effect=input2):
            add_new_item()
        self.assertEqual(test_inventory, return_inventory())
        
        #add furniture to inventory
        input3 = [3, 'couch', 20, 'y', 'leather', 'M']
        test_inventory = {1: {'productcode': 1, 'description': 'shoes',

                              'marketprice': 24, 'rentalprice': 10},

                          2: {'productcode': 2, 'description': 'Toaster',

                              'marketprice': 24, 'rentalprice': 10,

                              'brand': 'sony', 'voltage': 120},

                          3: {'productcode': 3, 'description': 'couch',

                              'marketprice': 24, 'rentalprice': 20,

                              'material': 'leather', 'size': 'M'}}

        with patch('builtins.input', side_effect=input3):
            add_new_item()
        self.assertEqual(test_inventory, return_inventory())

    def test_item_information(self):
        """Tests if item_info gets returned"""
        input1 = [1]
        with patch('builtins.input', side_effect=input1):
            self.assertEqual(item_info(), None)
            
    def test_system_exit(self):
        """ Tests main.exit_program."""
        with self.assertRaises(SystemExit):
            main.exit_program()




     
       
        

