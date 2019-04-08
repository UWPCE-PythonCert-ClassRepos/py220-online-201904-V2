'''
Electric appliances Class
'''

# Electric appliances class
from .inventoryclass import Inventory

class Electricappliances(Inventory):
    '''
    Class docstring
    '''
    def __init__(
            self,
            productcode,
            description,
            marketprice,
            rentalprice,
            brand,
            voltage):
        '''
        initializing variables
        '''

        super().__init__(productcode, description, marketprice, rentalprice)
        self.productcode = productcode
        self.description = description
        self.marketprice = marketprice
        self.rentalprice = rentalprice
        self.brand = brand
        self.voltage = voltage

    def returnasdictionary(self):
        '''
        method docstring
        '''

        outputdict = {}
        outputdict['productcode'] = self.productcode
        outputdict['description'] = self.description
        outputdict['marketprice'] = self.marketprice
        outputdict['rentalprice'] = self.rentalprice
        outputdict['brand'] = self.brand
        outputdict['voltage'] = self.voltage

        return outputdict
