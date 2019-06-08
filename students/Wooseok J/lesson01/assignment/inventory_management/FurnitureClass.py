""" Furniture class """
from inventory_class import Inventory


class Furniture(Inventory):
    """
    doc string
    """
    def __init__(self, product_code, description, market_price,
                 rental_price, material, size):

        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.material = material
        self.size = size
# creates instance variables

    def return_as_dictionary(self):
        """
        doc string
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size
        return output_dict

# returns dictionary
