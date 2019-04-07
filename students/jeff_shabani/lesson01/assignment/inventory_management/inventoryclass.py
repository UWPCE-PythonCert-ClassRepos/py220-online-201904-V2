"""
inventory module"""


class Inventory:
    """
    inventory framework"""

    def __init__(self, productcode, description, marketprice, rentalprice):
        self.productcode = productcode
        self.description = description
        self.marketprice = marketprice
        self.rentalprice = rentalprice

    def returnasdictionary(self):
        """
        populate inventory dictionary"""
        outputdict = {}
        outputdict['productcode'] = self.productcode
        outputdict['description'] = self.description
        outputdict['marketprice'] = self.marketprice
        outputdict['rentalprice'] = self.rentalprice

        return outputdict
