"""
    Autograde Lesson 8 assignment

"""

import pytest

import src.inventory as l


def test_add_furniture():
    """ testing add furniture fucntion"""
    # clean the file
    l.clean_file("rented_items.csv")
    l.add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    header = ("customer_name", "item_code", "item_description", "item_monthly_price")
    result = dict(zip(header, ("Elisa Miles", "LR04", "Leather Sofa", "25")))
    lines = l.read_csv("rented_items.csv")
    line = next(lines)
    assert line == result


def test_single_customer():
    items = [("Susan Wong", "LR01", "Small lamp", "7.50"),
             ("Susan Wong", "LR02", "Television", "28.00"),
             ("Susan Wong", "BR07", "LED lamp", "5.50"),
             ("Susan Wong", "KT08", "Basic refrigerator", "40.00")]
    header = ("customer_name", "item_code", "item_description", "item_monthly_price")
    results = (dict(i) for i in (zip(header, item) for item in items))
    l.clean_file("rented_items.csv")
    susan_furniture = l.single_customer("Susan Wong", "rented_items.csv")
    susan_furniture("test_items.csv")
    lines = l.read_csv("rented_items.csv")
    for line, result in zip(lines, results):
        assert line == result
