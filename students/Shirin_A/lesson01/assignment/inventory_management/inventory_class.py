""" Inventory class"""
class Inventory:
    """Inventory Class, contains all information about
       each item in the inventory """
    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """populate inventory dictionary"""
        output_dict = {}
        output_dict['productcode'] = self.product_code
        output_dict['description'] = self.description
        output_dict['marketprice'] = self.market_price
        output_dict['rentalprice'] = self.rental_price
        return output_dict
