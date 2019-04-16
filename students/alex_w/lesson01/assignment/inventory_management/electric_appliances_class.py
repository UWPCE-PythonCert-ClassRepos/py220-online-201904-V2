# Electric appliances class
from inventory_class import Inventory


class Electric_Appliances(Inventory):

    def __init__(self, product_code, description, market_price, rental_price, brand, voltage):
        super().__init__(product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        output_dict = super().return_as_dictionary()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
