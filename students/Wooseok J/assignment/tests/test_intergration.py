from unittest import TestCase
from unittest import mock
from main import main_menu


class TestClass(TestCase):
    """Integration tests for inventory_management"""

    def setup_method(self):
        """Initialize before each test method"""
        self.item_chair = {}
        self.item_microwave = ()
        self.item_microwave['product_code'] = 198
        self.item_microwave['description'] = 'Microwave'
        self.item_microwave['market_price'] = 200
        self.item_microwave['rental_price'] = 50
        self.item_microwave['brand'] = 'Samsung'
        self.item_microwave['voltage'] = 220

    @mock.patch('builtins.input')
    def test_mainmenu_1_electric(self, mocked_input):
        mocked_input.side_effect = ['1', '1', 'desc', 20, 'n', 'y', 'ge', 110]
        expect = main_menu()()
        Electricdic = {'1': {'ProductCode': '1', 'Description': 'desc',
                             'MarketPrice': 24, 'RentalPrice': 20,
                             'Brand': 'ge', 'Voltage': 110}}
        self.assertEqual(expect, Electricdic)

    def test_integration_chair(self):
        assert str(self.item_chair['product_code']) in self.inventory_string
        assert str(self.item_chair['description']) in self.inventory_string
        assert str(self.item_chair['market_price']) in self.inventory_string
        assert str(self.item_chair['rental_price']) in self.inventory_string

    def test_integration_microwave(self):
        assert str(self.item_microwave['product_code']) in self.inventory_string
        assert str(self.item_microwave['description']) in self.inventory_string
        assert str(self.item_microwave['market_price']) in self.inventory_string
        assert str(self.item_microwave['rental_price'])in self.inventory_string
        assert str(self.item_microwave['brand']) in self.inventory_string
        assert str(self.item_microwave['voltage']) in self.inventory_string
