#!/usr/bin/env python3
'''
Launches the user interface for the Inventory management system
'''
import sys
from market_prices import get_latest_price
from store_inventory import Inventory
from home_furniture import FurnitureClass
from electric_appliances import ElectricAppliances
FULL_INVENTORY = {}
'''
I don't like globals, but right now I can't think of how to fix this.
'''


def main_menu(user_prompt=None):
    '''
    Our main main
    '''
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options: {}"\
              .format(options_str))
        print("1. Add a new item to the Inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def get_price(item_code):
    '''
    Prints "Get Price", otherwise doesn't seem to do anything...
    '''
    # print("Get price")
    latest_price = get_latest_price(item_code)
    return latest_price


def add_new_item():
    '''
    Here we add a new individual item
    '''
    # global full_inventory
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        add_new_furnature(item_code, item_description, item_rental_price, \
        item_price)
    else:
        is_electric_appliance = input("Is this item an electric appliance? \
(Y/N): ")
        if is_electric_appliance.lower() == "y":
            add_new_electronics(item_code, item_description, \
            item_rental_price, item_price)
        else:
            new_item = Inventory(item_code, item_description,
                                 item_price, item_rental_price)
        FULL_INVENTORY[item_code] = new_item.return_as_dict()
        print("New Inventory item added")

def add_new_furnature(item_code, item_description, item_rental_price,
                      item_price):
    '''
    This is for adding furnature.  I've broken it out of the original format to
    fascilitate testing.
    '''
    item_material = input("Enter item material: ")
    item_size = input("Enter item size (S,M,L,XL): ")
    new_item = FurnitureClass(item_code, item_description,
                              item_price, item_rental_price,
                              item_material, item_size)
    FULL_INVENTORY[item_code] = new_item.return_as_dict()
    print("New Inventory item added")

def add_new_electronics(item_code, item_description, item_rental_price,
                        item_price):
    '''
    This is for adding electronics.  I've broken it out of the original format
    to fascilitate testing.
    '''
    item_brand = input("Enter item brand: ")
    item_voltage = input("Enter item voltage: ")
    new_item = ElectricAppliances(item_code,
                                  item_description, item_price,
                                  item_rental_price, item_brand,
                                  item_voltage)

    FULL_INVENTORY[item_code] = new_item.return_as_dict()
    print("New Inventory item added")

def item_info():
    '''
    This is where we enter the item information for new product
    '''
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        # pylint: disable=C0103
        for k, v in print_dict.items():
            print("{}:{}".format(k, v))
    else:
        print("Item not found in Inventory")


def exit_program():
    '''
    Gracefully exits
    '''
    sys.exit()


if __name__ == '__main__':
    # full_inventory = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
