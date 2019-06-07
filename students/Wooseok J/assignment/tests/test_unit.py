from unittest import TestCase
from inventory_class import Inventory
from market_prices import get_latest_price


class TestClass(TestCase):
    """Integration tests for inventory_management"""

    def test_inventory(self):
        ProductCode = 1
        Description = 'desk'
        MarketPrice = 59
        RentalPrice = 39
        inventory = Inventory(ProductCode, Description, MarketPrice, RentalPrice)
        self.assertEqual(ProductCode, inventory.productcode)
        self.assertEqual(Description, inventory.description)
        self.assertEqual(MarketPrice, inventory.marketprice)
        self.assertEqual(RentalPrice, inventory.rentalprice)
        self.assertEqual({'ProductCode': ProductCode, 'Description': Description,
                          'MarketPrice': MarketPrice, 'RentalPrice': RentalPrice},
                         inventory.returnasdictionary())

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

class market_priceTests(TestCase):
    def test_market_price(self):
        self.assertEqual(24, get_latest_price())