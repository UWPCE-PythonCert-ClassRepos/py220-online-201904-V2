"""
    Autograde Lesson 8 assignment

"""

import pytest
import inventory as l

@pytest.fixture
def _add_furniture():
    return ("../data/rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)


@pytest.fixture
def _single_customer():
    return ([['LR01','Small lamp',7.50],
             ['LR02','Television',28.00],
             ['BR07','LED lamp',5.50],
             ['KT08','Basic refrigerator',40.00]])


def test_add_furniture(_add_furniture):
    response = l.add_furniture("../data/rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    assert response == _add_furniture


def test_single_customer(_single_customer):
    create_invoice = l.single_customer("Susan Wong", "../data/rented_items.csv")
    response = create_invoice("../data/test_items.csv")
    assert response == _single_customer
