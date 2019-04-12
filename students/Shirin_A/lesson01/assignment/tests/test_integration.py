""" Integration test for inventory_management"""
# pylint: disable=C0303
from unittest.mock import patch
from unittest import TestCase
import pytest
import sys
#sys.path.append(r"C:\Users\Public\py220-online-201904-V2\students\Shirin_A\lesson01\assignment\inventory_management")
from main import add_new_item, return_inventory 
from main import item_info
#from electric_appliances import ElectricAppliances
#from furniture_class import Furniture  
from inventory_class import Inventory 
import market_prices


class IntegrationTest(TestCase):

    """Creates a class that tests inventory_management together"""

    def test_main_integration(self):

        """Test all functions with main as a starting point"""
        price = market_prices.get_latest_price(0)

        #Adding non categorized inventory item with main

        input1 = ['1', 'shoe', '1', 'n', 'n']
        item1 = Inventory('1', 'shoe', price, '1')
        with patch('builtins.input', side_effect=input1):
            add_new_item()            
        #Adding furniture item with main
        input2 = ['2', 'chair', '2', 'y', 'wood', 'S']        
        item2 = Furniture('2', 'chair', price, '2', 'wood', 'S')
        with patch('builtins.input', side_effect=input2):
            add_new_item()
        #Adding electric appliance with main
        input3 = ['3', 'stove', '3', 'n', 'y', 'LG', '100']
        item3 = ElectricAppliances('3', 'stove', price, '3', 'LG', '100')
        with patch('builtins.input', side_effect=input3):
            add_new_item()
        actual_inventory = return_inventory()
        expected_inventory = {
            '1': item1.return_as_dictionary(),
            '2': item2.return_as_dictionary(),
            '3': item3.return_as_dictionary()}
        self.assertEqual(actual_inventory, expected_inventory)
        
    def test_item_information(self):
        """Tests if item_info gets returned"""
        input1 = [10]
        with patch('builtins.input', side_effect=input1):
            self.assertEqual(item_info(), None)
            
      


        
