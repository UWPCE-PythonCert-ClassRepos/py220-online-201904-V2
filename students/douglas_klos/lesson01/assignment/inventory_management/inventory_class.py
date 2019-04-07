""" Inventory class """


class Inventory:
    """Inventory class

    Attributes:
        product_code (str) : Item code for product
        description (str) : Description of the item
        market_price (float) : Going market rate for item
        rental_price (float) : Rental price for the item

    """

    def __init__(self, product_code, description, market_price, rental_price):
        self.product_code = product_code
        self.description = description
        self.market_price = market_price
        self.rental_price = rental_price

    def return_as_dictionary(self):
        """Returns output_dict with contents of class attributes.

        Returns:
            dictionary containing the newly created item

        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price

        return output_dict
