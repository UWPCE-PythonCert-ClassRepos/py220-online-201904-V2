#!/usr/bin/env python3

'''note'''
from unittest import TestCase
from unittest import mock

#from ..inventory_management.main import mainmenu, add_new_item, item_info, exit_program
#from ..inventory_management.InventoryClass import Inventory
#from ..inventory_management.FurnitureClass import Furniture
#from ..inventory_management.ElectricAppliancesClass import ElectricAppliances
#from ..inventory_management.market_prices import get_latest_price

from main import mainmenu, add_new_item, item_info, exit_program
from InventoryClass import Inventory
from FurnitureClass import Furniture
from ElectricAppliancesClass import ElectricAppliances
from market_prices import get_latest_price


class InventoryTests(TestCase):
    '''doc string'''
    def test_inventory(self):
        '''doc string'''
        ProductCode = 1
        Description = 'desc'
        MarketPrice = 40
        RentalPrice = 20
        inventory = Inventory(ProductCode, Description, MarketPrice, RentalPrice)
        self.assertEqual(ProductCode, inventory.productcode)
        self.assertEqual(Description, inventory.description)
        self.assertEqual(MarketPrice, inventory.marketprice)
        self.assertEqual(RentalPrice, inventory.rentalprice)
        self.assertEqual({'ProductCode': ProductCode, 'Description': Description,
                          'MarketPrice': MarketPrice, 'RentalPrice': RentalPrice},
                         inventory.returnasdictionary())


class FurnitureTests(TestCase):
    '''doc'''
    def test_furniture(self):
        '''doc string'''
        ProductCode = 1
        Description = 'desc'
        MarketPrice = 40
        RentalPrice = 20
        Material = 'wood'
        Size = 'M'
        furniture = Furniture(ProductCode, Description, MarketPrice, RentalPrice, Material, Size)
        self.assertEqual({'ProductCode': ProductCode, 'Description': Description,
                          'MarketPrice': MarketPrice, 'RentalPrice': RentalPrice,
                          'Material': Material, 'Size': Size}, furniture.returnasdictionary())


class ElectricAppliancesTests(TestCase):
    '''doc'''
    def test_electricappliances(self):
        '''doc string'''
        #self.adder.calc = MagicMock(return_value=0)
        ProductCode = 1
        Description = 'desc'
        MarketPrice = 40
        RentalPrice = 20
        Brand = 'GE'
        Voltage = 110
        electricapp = ElectricAppliances(ProductCode, Description, MarketPrice,
                                         RentalPrice, Brand, Voltage)
        self.assertEqual({'ProductCode': ProductCode, 'Description': Description,
                          'MarketPrice': MarketPrice, 'RentalPrice': RentalPrice,
                          'Brand': Brand, 'Voltage': Voltage}, electricapp.returnasdictionary())


class market_priceTests(TestCase):
    '''doc string'''
    def test_market_price(self):
        '''doc string'''
        self.assertEqual(24, get_latest_price())


class mainTests(TestCase):
    '''doc string'''
    ########## test add_new_item #####################################
    @mock.patch('builtins.input')
    def test_add_new_item_inventory(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['1', 'desc', 20, 'n', 'n']
        expect = add_new_item()
        InventoryDic = {'1':{'ProductCode': '1', 'Description': 'desc',
                             'MarketPrice': 24, 'RentalPrice': 20}}
        self.assertEqual(expect, InventoryDic)

    @mock.patch('builtins.input')
    def test_add_new_item_furniture(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['1', 'desc', 20, 'y', 'wood', 'M']
        expect = add_new_item()
        FurnitureDic = {'1':{'ProductCode': '1', 'Description': 'desc',
                             'MarketPrice': 24, 'RentalPrice': 20,
                             'Material': 'wood', 'Size': 'M'}}
        self.assertEqual(expect, FurnitureDic)

    @mock.patch('builtins.input')
    def test_add_new_item_electricapp(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['1', 'desc', 20, 'n', 'y', 'ge', 110]
        expect = add_new_item()
        ElectricDic = {'1':{'ProductCode': '1', 'Description': 'desc',
                            'MarketPrice': 24, 'RentalPrice': 20,
                            'Brand': 'ge', 'Voltage': 110}}
        self.assertEqual(expect, ElectricDic)

    ############ test item_info ###############################
    @mock.patch('builtins.input')
    def test_item_info(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['1']
        expect = item_info()
        InventoryDic = {'1':{'ProductCode': '1', 'Description': 'desc',
                             'MarketPrice': 24, 'RentalPrice': 20}}
        self.assertEqual(expect, InventoryDic)

    ############ test exit_program #########################
    def test_exit_program(self):
        '''doc string'''
        with self.assertRaises(SystemExit):
            exit_program()

    ############ test mainmenu #########################
    @mock.patch('builtins.input')
    def test_mainmenu_1(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['1']
        expect = mainmenu()
        self.assertEqual(expect, add_new_item)

    @mock.patch('builtins.input')
    def test_mainmenu_2(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['2']
        expect = mainmenu()
        self.assertEqual(expect, item_info)

    @mock.patch('builtins.input')
    def test_mainmenu_q(self, mocked_input):
        '''doc string'''
        mocked_input.side_effect = ['q']
        expect = mainmenu()
        self.assertEqual(expect, exit_program)
