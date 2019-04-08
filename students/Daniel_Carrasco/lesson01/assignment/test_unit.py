from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.electricappliancesclass import Electricappliances as eac
from inventory_management.furnitureclass import Furniture as fc
from inventory_management.inventoryclass import Inventory as ic
from inventory_management.market_prices import get_latest_price as glp
import inventory_management.main as mm

class ElectricappliancesTest(TestCase):
    '''
    class docstring
    '''
    def test_eacdict(self):
        test_dict = {
                    'productcode': 'AB123',
                    'description': 'TEST',
                    'marketprice': '150.00',
                    'rentalprice': '50.25',
                    'brand': 'TEST',
                    'voltage': '321'}
        input_dict = eac('AB123', 'TEST', '150.00', '50.25', 'TEST', '321').returnasdictionary()
        self.assertEqual(input_dict,test_dict)


class FurnitureclassTest(TestCase):
    '''
    class docstring
    '''
    def test_fcdict(self):
        test_dict = {
                    'productcode': 'AB123',
                    'description': 'TEST',
                    'marketprice': '150.00',
                    'rentalprice': '50.25',
                    'material': 'TEST',
                    'size': '321'}
        input_dict = fc('AB123', 'TEST', '150.00', '50.25', 'TEST', '321').returnasdictionary()
        self.assertEqual(input_dict,test_dict)


class InventoryclassTest(TestCase):
    '''
    class docstring
    '''
    def test_icdict(self):
        test_dict = {
                    'productcode': 'AB123',
                    'description': 'TEST',
                    'marketprice': '150.00',
                    'rentalprice': '50.25',
                    }
        input_dict = ic('AB123', 'TEST', '150.00', '50.25').returnasdictionary()
        self.assertEqual(input_dict,test_dict)

class MarketpriceTest(TestCase):
    '''
    class docstring
    '''
    def test_mp(self):
        test_mp = 24
        input_mp = glp('test')
        self.assertEqual(test_mp,input_mp)

class MainmenuTest(TestCase):
    '''
    class docstring
    '''
    def test_mainmenu(self):
        with patch('builtins.input', return_value = '1'):
            assert input() == '1'
        with patch('builtins.input', return_value = '2'):
            assert input() == '2'
        with patch('builtins.input', return_value = '3'):
            assert input() == '3'

    def test_getprice(self):
        test_gp = mm.getprice('test1')
        input_gp = mm.getprice('test2')
        self.assertEqual(test_gp,input_gp)

    def test_iteminfo(self):
        with patch('builtins.input', return_value = 'test1'):
            test_ii = mm.iteminfo()
        with patch('builtins.input', return_value = 'test2'):
            input_ii = mm.iteminfo()
        self.assertEqual(test_ii,input_ii)

    def test_exit(self):
        '''
        method docstring
        '''
        with self.assertRaises(SystemExit) as testexit:
            mm.exitprogram()
            self.assertEqual(testexit.exception.code, 1)

        def test_add_new(self):
            """
            Tests for menu item 1 selection"""
            while True:
                try:
                    with patch('builtins.input', side_effect='1'):
                        self.assertEqual(mm.mainmenu(), mm.addnewitem())
                except StopIteration as error:
                    return error






