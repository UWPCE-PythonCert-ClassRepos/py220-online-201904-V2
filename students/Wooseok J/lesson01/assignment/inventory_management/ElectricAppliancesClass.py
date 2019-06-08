""" Electric Appliances Class """

from inventory_class import Inventory


class ElectricAppliances(Inventory):
    """
    doc string
    """
    def __init__(self, product_code, description, market_price,
                 rental_price, brand, voltage):
        """
        doc string
        """
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.brand = brand
        self.voltage = voltage

    def return_as_dict(self):
        """
        doc string
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
# return dict
