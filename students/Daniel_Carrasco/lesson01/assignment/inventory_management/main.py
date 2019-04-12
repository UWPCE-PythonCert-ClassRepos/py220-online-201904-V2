'''
Module Docstring
'''
# Launches the user interface for the inventory management system
import sys
from inventory_management import market_prices
from inventory_management import inventoryclass
from inventory_management import furnitureclass
from inventory_management import electricappliancesclass

FULL_INVENTORY = {}


def mainmenu(user_prompt=None):
    '''
    method docstring
    '''

    valid_prompts = {"1": addnewitem,
                     "2": iteminfo,
                     "q": exitprogram}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options) - 1)).format(*options)
        print("Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def getprice(itemcode):
    '''
    method docstring
    '''

    print("Get price")


def addnewitem():
    '''
    method docstring
    '''

    itemcode = input("Enter item code: ")
    itemdescription = input("Enter item description: ")
    itemrentalprice = input("Enter item rental price: ")

    # Get price from the market prices module
    itemprice = market_prices.get_latest_price(itemcode)

    isfurniture = input("Is this item a piece of furniture? (Y/N): ")
    if isfurniture.lower() == "y":
        itemmaterial = input("Enter item material: ")
        itemsize = input("Enter item size (S,M,L,XL): ")
        newitem = furnitureclass.Furniture(
            itemcode,
            itemdescription,
            itemprice,
            itemrentalprice,
            itemmaterial,
            itemsize)
    else:
        iselectricappliance = input(
            "Is this item an electric appliance? (Y/N): ")
        if iselectricappliance.lower() == "y":
            itembrand = input("Enter item brand: ")
            itemvoltage = input("Enter item voltage: ")
            newitem = electricappliancesclass.Electricappliances(
                itemcode,
                itemdescription,
                itemprice,
                itemrentalprice,
                itembrand,
                itemvoltage)
        else:
            newitem = inventoryclass.Inventory(
                itemcode, itemdescription, itemprice, itemrentalprice)
    FULL_INVENTORY[itemcode] = newitem.returnasdictionary()
    print("New inventory item added")


def iteminfo():
    '''
    method docstring
    '''

    itemcode = input("Enter item code: ")
    if itemcode in FULL_INVENTORY:
        printdict = FULL_INVENTORY[itemcode]
        for key, value in printdict.items():
            print("{}:{}".format(key, value))
    else:
        print("Item not found in inventory")


def exitprogram():
    '''
    method docstring
    '''

    sys.exit()


if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        mainmenu()()
        input("Press Enter to continue...........")
