'''doc string'''
# Electric appliances class
from InventoryClass import Inventory

class ElectricAppliances(Inventory):
    '''doc string'''
    def __init__(self, productcode, description, marketprice,
                 rentalprice, brand, voltage):
        '''doc string'''
        Inventory.__init__(self, productcode, description, marketprice,
                           rentalprice)
        # Creates common instance variables from the parent class

        self.brand = brand
        self.voltage = voltage

    def returnasdictionary(self):
        '''doc string'''
        outputdict = Inventory.returnasdictionary(self)
        outputdict['Brand'] = self.brand
        outputdict['Voltage'] = self.voltage

        return outputdict
