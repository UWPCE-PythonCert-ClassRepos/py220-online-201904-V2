"""
Tests for basic_operations.py

These tests will only pass when run on an empty database.
"""

import pytest
import basic_operations as bo


@pytest.fixture
def _update_customer_credit():
    return [
        ("598", "Name", "Lastname", "Address", "phone", "email", "active", 999),
    ]

@pytest.fixture
def _list_active_customers():
    return [
        ("598", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("597", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("596", "Name", "Lastname", "Address", "phone", "email", "inactive", 99),
        ("595", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("594", "Name", "Lastname", "Address", "phone", "email", "active", 10),
        ("593", "Name", "Lastname", "Address", "phone", "email", "active", 99)
    ]


def test_update_customer_credit(_update_customer_credit):
    """
    Test to ensure update_customer_credit modifies credit_limit accurately.
    """
    for customer in _update_customer_credit:
        bo.add_customer(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[4],
            customer[5],
            customer[6],
            customer[7]
        )

    bo.update_customer_credit("598", 110)
    updated_cust = bo.CustomerCredit.select().join(
        bo.Customer).where(bo.Customer.customer_id == '598')
    assert updated_cust[0].credit_limit == 110

    with pytest.raises(ValueError) as execinfo:
        bo.update_customer_credit("11111", 456)
        assert 'NoCustomer' in str(execinfo.value)

    bo.delete_customer('598')

    assert bo.list_active_customers() == 0

def test_list_active_users(_list_active_customers):
    """ Testing to ensure users status is set and retrieved properly. """
    for customer in _list_active_customers:
        bo.add_customer(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[4],
            customer[5],
            customer[6],
            customer[7]
        )

    assert bo.list_active_customers() == 4

    for customer in _list_active_customers:
        bo.delete_customer(customer[0])
    
    assert bo.list_active_customers() == 0