"""Launches the user interface for the inventory management system"""
import sys
from market_prices import get_latest_price
from inventory_management import inventory_class
from inventory_management import furniture_class
from inventory_management import electric_appliances_class

FULL_INVENTORY = {}


"""Main menu options"""


def main_menu(user_prompt=None):
    """User prompts"""
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options) - 1)).format(*options)
        print("Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def get_price():
    """Get price"""
    print("Get price")


def add_new_item():
    """Add new item"""
    # global FULL_INVENTORY
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")


    # Get price from the market prices module
    item_price = get_latest_price(item_code)

    is_furniture = input("Is this item a piece of is_furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = furniture_class.Furniture(
            item_code, item_description, item_price, item_rental_price,
            item_material, item_size)
    else:
        is_electric_appliances = input(
            "Is this item an electric appliance? (Y/N): ")
        if is_electric_appliances.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = electric_appliances_class.Electric_Appliances(
                item_code, item_description, item_price, item_rental_price,
                item_brand, item_voltage)
        else:
            new_item = inventory_class.Inventory(
                item_code, item_description, item_price, item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """Item for product"""
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for key, value in print_dict.items():
            print("{}:{}".format(key, value))
    else:
        print("Item not found in inventory")


def exit_program():
    """Exit the program"""
    sys.exit()


if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
