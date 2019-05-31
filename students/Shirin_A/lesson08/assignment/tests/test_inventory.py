"""
    Autograde Lesson 8 assignment

"""

import pytest
import inventory as I


@pytest.fixture
def _add_furniture():
    return ("../data/invoice_file.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)


@pytest.fixture
def _single_customer():
    return ([['LR01', 'Small lamp', 7.5],

             ['LR02', 'Television', 28.0],

             ['BR07', 'LED lamp', 5.5],

             ['KT08', 'Basic refrigerator', 40.0]])


def test_add_furniture(_add_furniture):
    """test add_furniture"""
    response = I.add_furniture("../data/invoice_file.csv", "Elisa Miles",
                               "LR04", "Leather Sofa", 25)
    assert response == _add_furniture

def test_single_customer(_single_customer):
    """test single_customer"""
    create_invoice = I.single_customer("Susan Wong", "../data/invoice_file.csv")
    response = create_invoice("../data/test_items.csv")
    assert response == _single_customer
