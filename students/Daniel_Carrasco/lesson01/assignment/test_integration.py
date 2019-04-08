from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.electricappliancesclass import Electricappliances as eac
from inventory_management.furnitureclass import Furniture as fc
from inventory_management.inventoryclass import Inventory as ic
from inventory_management.market_prices import get_latest_price as glp
import inventory_management.main as mm

class ModuleTest(TestCase):
    test_eadict = {
                'productcode': 'AB123',
                'description': 'TEST',
                'marketprice': '150.00',
                'rentalprice': '50.25',
                'brand': 'TEST',
                'voltage': '321'
                }
    test_fdict = {
                'productcode': 'AB123',
                'description': 'TEST',
                'marketprice': '150.00',
                'rentalprice': '50.25',
                'material': 'TEST',
                'size': '321'
                }
    test_dict = {
                'productcode': 'AB123',
                'description': 'TEST',
                'marketprice': '150.00',
                'rentalprice': '50.25',
                }
    @patch('inventory_management.main.addnewitem', return_value=test_dict)
    def test_main(self, addnewitem):
        '''
        method doc string
        '''

        dict_inv = {
                    'productcode': 'AB123',
                    'description': 'TEST',
                    'marketprice': '150.00',
                    'rentalprice': '50.25',
                    }
        self.assertEqual(addnewitem(), dict_inv)