'''doc string'''
# Inventory class
class Inventory:
    '''doc string'''
    def __init__(self, ProductCode, Description, MarketPrice, RentalPrice):
        '''doc string'''
        self.productcode = ProductCode
        self.description = Description
        self.marketprice = MarketPrice
        self.rentalprice = RentalPrice

    def returnasdictionary(self):
        '''doc string'''
        outputdict = {}
        outputdict['ProductCode'] = self.productcode
        outputdict['Description'] = self.description
        outputdict['MarketPrice'] = self.marketprice
        outputdict['RentalPrice'] = self.rentalprice

        return outputdict
