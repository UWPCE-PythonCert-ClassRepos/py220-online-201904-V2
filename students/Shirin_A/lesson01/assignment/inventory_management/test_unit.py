
import pytest 
from unittest.mock import patch, MagicMock
from unittest import TestCase 
from electric_appliances import ElectricAppliances
from furniture_class import Furniture
from inventory_class import Inventory
import main
import market_prices

class ElectricAppliancesTest(TestCase): 
    
    def test_electric_appliances(self):
        electric_test = ElectricAppliances('340', 'Toaster', '24', '15.00',
                                           'frizi', '220')                                     
        electric_dict_test = electric_test.return_as_dictionary() 
        self.assertEqual(electric_dict_test, {'product_code': '340', 
                                              'description': 'Toaster', 

                                              'market_price': '24', 

                                              'rental_price': '15.00',
                                              'brand': 'frizi', 
                                              'voltage': '220'}) 


class InventoryTest(TestCase): 
    ''' 
    Testing inventory class
    ''' 
    def test_inventory(self):
        inventory_test = Inventory('5122', 'toaster', '24.00', '15.00')             
        furniture_dict_test = inventory_test.return_as_dictionary() 
        self.assertEqual(furniture_dict_test, {'product_code': '5122',
                                               'description': 'Toaster',

                                               'market_price': '24', 
                                               'rental_price': '15.00'})
        
class MarketPricesTest(TestCase):
    """testing market price"""    
    def test_market_price(self):
         prices = market_prices.get_latest_price('550')         
         self.assertEqual(prices, 24)
        

       



       
