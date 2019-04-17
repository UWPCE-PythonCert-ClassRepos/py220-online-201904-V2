#!/usr/bin/env python3

'''mod string'''
from unittest import TestCase
from unittest import mock

#from ..inventory_management.main import mainmenu
from main import mainmenu
#import main


class ModuleTests(TestCase):
    '''doc string'''
    @mock.patch('builtins.input')
    def test_mainmenu_1_inventory(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['1', '1', 'desc', 20, 'n', 'n']
        expect = mainmenu()()
        InventoryDic = {'1':{'ProductCode': '1', 'Description': 'desc',
                             'MarketPrice': 24, 'RentalPrice': 20}}
        self.assertEqual(expect, InventoryDic)

    @mock.patch('builtins.input')
    def test_mainmenu_1_furniture(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['1', '1', 'desc', 20, 'y', 'wood', 'M']
        expect = mainmenu()()
        FurnitureDic = {'1': {'ProductCode': '1', 'Description': 'desc',
                              'MarketPrice': 24, 'RentalPrice': 20,
                              'Material': 'wood', 'Size': 'M'}}
        self.assertEqual(expect, FurnitureDic)

    @mock.patch('builtins.input')
    def test_mainmenu_1_electric(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['1', '1', 'desc', 20, 'n', 'y', 'ge', 110]
        expect = mainmenu()()
        ElectricDic = {'1': {'ProductCode': '1', 'Description': 'desc',
                             'MarketPrice': 24, 'RentalPrice': 20,
                             'Brand': 'ge', 'Voltage': 110}}
        self.assertEqual(expect, ElectricDic)

    @mock.patch('builtins.input')
    def test_mainmenu_2(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['2', '1']
        expect = mainmenu()()
        InventoryDic = {'1':{'ProductCode': '1', 'Description': 'desc',
                             'MarketPrice': 24, 'RentalPrice': 20}}
        self.assertEqual(expect, InventoryDic)

    @mock.patch('builtins.input')
    def test_mainmenu_q(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['q']
        with self.assertRaises(SystemExit):
            mainmenu()()
