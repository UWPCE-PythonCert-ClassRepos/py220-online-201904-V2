"""
Launches the user interface for the inventory management system
"""
import sys

from electricappliancesclass import ElectricAppliances
from furnitureclass import Furniture
from inventoryclass import Inventory
from market_prices import get_latest_price

FULLINVENTORY = dict()

"""
Moved prompt text here for testing"""
OPTIONS_STR = '({options_str})'
PROMPT_TEXT = f'Please choose from the following options {OPTIONS_STR}:\n' \
    f'1. Add a new item to the inventory\n2. Get item ' \
    f'information\nq. Quit'


def mainmenu(user_prompt=None):
    """
    main menu for program"""
    valid_prompts = {"1": addnewitem,
                     "2": iteminfo,
                     "q": exitprogram}

    while user_prompt not in valid_prompts:
        print(PROMPT_TEXT)
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def main_menu_for_testing():
    """
    Function used to test main menu console display"""
    print(PROMPT_TEXT)


def getprice():
    """
    function to get price"""

    print("Get price")
    latest_price = get_latest_price(item_code)
    return latest_price


def add_non_furniture_nor_appliance(itemcode, itemdescription,
                                    itemprice, itemrentalprice):
    """This function adds an item that's neither furniture
    nor an applicance
    """

    newitem = Inventory(itemcode, itemdescription,
                        itemprice, itemrentalprice)
    FULLINVENTORY[itemcode] = newitem.returnasdictionary()


def add_furniture(itemcode, description, marketprice, rentalprice):
    """
    This function adds a new piece of furniture"""

    material = input("Enter item material: ")
    size = input("Enter item size (S,M,L,XL): ")
    newitem = Furniture(itemcode, description,
                        marketprice, rentalprice
                        , material, size)
    FULLINVENTORY[itemcode] = newitem.returnasdictionary()
    print("New inventory item added")


def add_appliance(itemcode, description, marketprice, rentalprice):
    """
    This function adds a new appliance"""

    itembrand = input("Enter item brand: ")
    itemvoltage = input("Enter item voltage: ")
    newitem = ElectricAppliances \
        (itemcode, description, marketprice, rentalprice,
         itembrand, itemvoltage)

    FULLINVENTORY[itemcode] = newitem.returnasdictionary()
    print("New inventory item added")


def addnewitem():
    """
    function to add new item"""

    itemcode = input("Enter item code: ")
    itemdescription = input("Enter item description: ")
    itemrentalprice = input("Enter item rental price: ")

    # Get price from the market prices module
    itemprice = get_latest_price(itemcode)

    isfurniture = input("Is this item a piece of furniture? (Y/N): ")
    if isfurniture.lower() == "y":
        add_furniture(itemcode, itemdescription, itemprice, itemrentalprice)
    else:
        iselectricappliance = input("Is this item an electric appliance?"
                                    " (Y/N): ")
        if iselectricappliance.lower() == "y":
            add_appliance(itemcode, itemdescription, itemprice, itemrentalprice)
    add_non_furniture_nor_appliance(itemcode, itemdescription, itemprice,
                                    itemrentalprice)
    print("New inventory item added")


def iteminfo():
    """This function gets item information from
    user input.
    """
    itemcode = input("Enter item code: ")
    if itemcode in FULLINVENTORY:
        printdict = FULLINVENTORY[itemcode]
        for key, value in printdict.items():
            print("{}:{}".format(key, value))
    else:
        print("Item not found in inventory")


def exitprogram():
    """
    function to exit the program"""
    sys.exit()


if __name__ == '__main__':
    while True:
        mainmenu()()
        input("Press Enter to continue...........")
