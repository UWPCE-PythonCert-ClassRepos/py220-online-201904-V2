"""
Electric appliances module"""

from students.jeff_shabani.lesson01.assignment.inventory_management.inventoryclass import *


class ElectricAppliances(Inventory):
    """
    Creates the electrical appliances class"""

    def __init__(self, productcode, description, marketprice, rentalprice
                 , brand, voltage):
        super().__init__(productcode, description, marketprice, rentalprice)
        self.brand = brand
        self.voltage = voltage

    def returnasdictionary(self):
        """
        populates dictionary with arguments"""
        outputdict = super().returnasdictionary()
        outputdict['brand'] = self.brand
        outputdict['voltage'] = self.voltage

        return outputdict
