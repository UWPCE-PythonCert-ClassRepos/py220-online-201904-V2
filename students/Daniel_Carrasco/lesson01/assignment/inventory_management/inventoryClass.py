'''
Inventory Class
'''

# Inventory class


class Inventory:
    '''
    Class for inventory
    '''

    def __init__(self, productcode, description, marketprice, rentalprice):
        '''
        initializing variables
        '''

        self.productcode = productcode
        self.description = description
        self.marketprice = marketprice
        self.rentalprice = rentalprice

    def returnasdictionary(self):
        '''
        returns as dictionary
        '''

        outputdict = {}
        outputdict['productcode'] = self.productcode
        outputdict['description'] = self.description
        outputdict['marketprice'] = self.marketprice
        outputdict['rentalprice'] = self.rentalprice

        return outputdict
