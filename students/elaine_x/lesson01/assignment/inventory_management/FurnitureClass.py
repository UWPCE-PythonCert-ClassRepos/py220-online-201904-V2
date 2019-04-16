'''doc string'''
# Furniture class
from InventoryClass import Inventory

class Furniture(Inventory):
    '''doc string'''
    def __init__(self, productcode, description, marketprice, rentalprice,
                 material, size):
        '''doc string'''
        Inventory.__init__(self, productcode, description, marketprice,
                           rentalprice)
        # Creates common instance variables from the parent class

        self.material = material
        self.size = size

    def returnasdictionary(self):
        '''doc string'''
        outputdict = Inventory.returnasdictionary(self)

        outputdict['Material'] = self.material
        outputdict['Size'] = self.size

        return outputdict
