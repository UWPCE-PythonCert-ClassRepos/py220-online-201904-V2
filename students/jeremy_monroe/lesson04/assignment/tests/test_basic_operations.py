import pytest
import basic_operations as bo


@pytest.fixture
def _save_customer():
    return [
        ("598", "Charles", "Lastname", "Address", "phone", "email", "active", 999),
        ("597", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("596", "Naomi", "Lastname", "Address", "phone", "email", "inactive", 99),
        ("595", "Nantucket", "Lastname", "Address", "phone", "email", "active", 999),
        ("594", "Name", "Lastname", "Address", "phone", "email", "active", 10),
        ("593", "Narwhal", "Lastname", "Address", "phone", "email", "active", 99)
    ]


@pytest.fixture
def _save_customer_credit_limit():
    return [
        ("123", "Nancy", "Lastname", "Address", "phone", "email", "active", 999),
        ("456", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("123", "Nicholas", "Lastname", "Address", "phone", "email", "active", 999),
        ("789", "Name", "Lastname", "Address", "phone", "email", "active", 0),
        ("345", "Nearsighted", "Lastname",
         "Address", "phone", "email", "active", -10),
        ("0123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("777", "Nameless", "Lastname", "Address", "phone", "email", "active", 999)
    ]


@pytest.fixture
def _save_customer_status(): # needs to del with database
    return [
        ("798", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("797", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("796", "Name", "Lastname", "Address", "phone", "email", "inactive", -99)
    ]


def test_save_customer(_save_customer):
    """
    Tests the save customer function.
    And at the same time the delete_customer function.
    """
    for customer in _save_customer:
        bo.save_customer(
            customer[0], customer[1], customer[2], customer[3], customer[4],
            customer[5])

    test_cust = bo.Customer.get(bo.Customer.customer_id == '598')
    assert test_cust.name == 'Charles'

    for customer in _save_customer:
        bo.delete_customer(customer[0])

    test_empty = bo.Customer.select()
    assert len(test_empty) == 0


def test_save_credit_limit(_save_customer_credit_limit):
    """
    Tests save_credit_limit.
    Requires Customers saved to db to work correctly.
    """
    for cust in _save_customer_credit_limit:
        bo.save_customer(
            cust[0], cust[1], cust[2], cust[3], cust[4],
            cust[5])

    for cust in _save_customer_credit_limit:
        current_cust = bo.Customer.get(bo.Customer.customer_id == cust[0])
        bo.save_credit_limit(current_cust, cust[7])

    test_cust = bo.CustomerCredit.get(
        bo.CustomerCredit.customer == bo.Customer.get(bo.Customer.customer_id == '777'))
    assert test_cust.credit_limit == 999

    for customer in _save_customer_credit_limit:
        bo.delete_customer(customer[0])

    test_empty = bo.Customer.select()
    assert len(test_empty) == 0


def test_save_customer_status(_save_customer_status):
    """
    Tests save_customer_status.
    Requires Customers saved to db to work correctly.
    """    
    for cust in _save_customer_status:
        bo.save_customer(
            cust[0], cust[1], cust[2], cust[3], cust[4],
            cust[5])

    for cust in _save_customer_status:
        current_cust = bo.Customer.get(bo.Customer.customer_id == cust[0])
        bo.save_customer_status(current_cust, cust[6])

    test_cust = bo.CustomerStatus.get(
        bo.CustomerStatus.customer == bo.Customer.get(bo.Customer.customer_id == '797'))
    assert test_cust.status == 'inactive'

    for customer in _save_customer_status:
        bo.delete_customer(customer[0])

    test_empty = bo.Customer.select()
    assert len(test_empty) == 0
