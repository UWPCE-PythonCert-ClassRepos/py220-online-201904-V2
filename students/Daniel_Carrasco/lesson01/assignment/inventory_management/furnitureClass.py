'''
Furniture Class
'''

# Furniture class
from .inventoryclass import Inventory


class Furniture(Inventory):
    '''
    Class for inventory
    '''

    def __init__(
            self,
            productcode,
            description,
            marketprice,
            rentalprice,
            material,
            size):
        '''
        initializing variables
        '''

        super().__init__(productcode, description, marketprice, rentalprice)
        self.productcode = productcode
        self.description = description
        self.marketprice = marketprice
        self.rentalprice = rentalprice
        self.material = material
        self.size = size

    def returnasdictionary(self):
        '''
        return as dictionary
        '''

        outputdict = {}
        outputdict['productcode'] = self.productcode
        outputdict['description'] = self.description
        outputdict['marketprice'] = self.marketprice
        outputdict['rentalprice'] = self.rentalprice
        outputdict['material'] = self.material
        outputdict['size'] = self.size

        return outputdict
