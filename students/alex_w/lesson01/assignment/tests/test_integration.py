from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import Electric_Appliances


class TestClass():
    """Integration tests for inventory_management"""

    def setup_method(self):
        """Initialize before each test method"""
        self.item_chair = {}
        self.item_microwave = {}

        self.item_microwave['product_code'] = 200
        self.item_microwave['description'] = 'Microwave'
        self.item_microwave['market_price'] = 222
        self.item_microwave['rental_price'] = 22
        self.item_microwave['brand'] = 'LG'
        self.item_microwave['voltage'] = 230


    def test_integration_chair(self):
        """Integration test for chair inventory

        Verifies that all chair related data is present.

        """
        assert str(self.item_chair['product_code']) in self.inventory_string
        assert str(self.item_chair['description']) in self.inventory_string
        assert str(self.item_chair['market_price']) in self.inventory_string
        assert str(self.item_chair['rental_price']) in self.inventory_string

    def test_integration_microwave(self):
        """Integration test for microwave electrical applicance"""
        assert str(self.item_microwave['product_code']) in self.inventory_string
        assert str(self.item_microwave['description']) in self.inventory_string
        assert str(self.item_microwave['market_price']) in self.inventory_string
        assert str(self.item_microwave['rental_price'])in self.inventory_string
        assert str(self.item_microwave['brand']) in self.inventory_string
        assert str(self.item_microwave['voltage']) in self.inventory_string


