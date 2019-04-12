#!/usr/bin/env python3
'''Launches the user interface for the inventory management system'''
import sys
from market_prices import get_latest_price
from InventoryClass import Inventory
from FurnitureClass import Furniture
from ElectricAppliancesClass import ElectricAppliances

def mainmenu(user_prompt=None):
    '''doc string'''
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options:", ({options_str}))
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

#def getPrice():
#    '''doc string'''
#    print("Get price")

FULLINVENTORY = {}

def add_new_item():
    '''doc string'''

    itemcode = input("Enter item code: ")
    itemdescription = input("Enter item description: ")
    itemrentalprice = input("Enter item rental price: ")

    # Get price from the market prices module
    itemprice = get_latest_price()

    isfurniture = input("Is this item a piece of furniture? (Y/N): ")
    if isfurniture.lower() == "y":
        itemmaterial = input("Enter item material: ")
        itemsize = input("Enter item size (S,M,L,XL): ")
        newitem = Furniture(itemcode, itemdescription,
                            itemprice, itemrentalprice,
                            itemmaterial, itemsize)
    else:
        iselectricappliance = input("Is this item an electric appliance?"
                                    " (Y/N): ")
        if iselectricappliance.lower() == "y":
            itembrand = input("Enter item brand: ")
            itemvoltage = input("Enter item voltage: ")
            newitem = ElectricAppliances\
                (itemcode, itemdescription, itemprice,
                 itemrentalprice, itembrand, itemvoltage)
        else:
            newitem = Inventory(itemcode, itemdescription,
                                itemprice, itemrentalprice)
    FULLINVENTORY[itemcode] = newitem.returnasdictionary()
    print("New inventory item added")
    return FULLINVENTORY

def item_info():
    '''doc string'''
    itemcode = input("Enter item code: ")
    if itemcode in FULLINVENTORY:
        printdict = FULLINVENTORY[itemcode]
        for k, val in printdict.items():
            print("{}:{}".format(k, val))
    else:
        print("Item not found in inventory")
    return FULLINVENTORY

def exit_program():
    '''doc string'''
    sys.exit()

if __name__ == '__main__':

    while True:
        print(FULLINVENTORY)
        mainmenu()()
        input("Press Enter to continue...........")
