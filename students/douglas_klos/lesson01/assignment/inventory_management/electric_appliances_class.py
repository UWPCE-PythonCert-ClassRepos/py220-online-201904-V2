""" Electric appliances class """

from .inventory_class import Inventory


class ElectricAppliances(Inventory):
    """Electric Appliances class, inerits from Inventory.

    Attributes:
        brand (str) : Brand of the electric appliance
        voltage (int) : Voltage of the electric appliance

    """

    def __init__(self, product_code, description,
                 market_price, rental_price, brand, voltage):
        # Creates common instance variables from the parent class
        super().__init__(product_code, description, market_price, rental_price)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        """Returns output_dict with contents of class attributes.

        Returns:
            dictionary containing the newly created item

        """
        output_dict = super().return_as_dictionary()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
