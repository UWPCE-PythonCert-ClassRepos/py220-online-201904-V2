"""
Integration testing for basic_operations in conjunction with customer_models.

This test will only pass when run on an empty database as well.
"""

import pytest
import basic_operations as bo

@pytest.fixture
def _integration_test_filler():
    return [
        ("598", "Jim", "Lastname", "Address", "phone", "email", "active", 999),
        ("597", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("596", "James", "Lastname", "Address", "phone", "email", "inactive", 99),
        ("595", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("594", "Ronald", "Lastname", "Address", "phone", "email", "active", 10),
        ("593", "Name", "Lastname", "Address", "phone", "email", "active", 99),
        ("798", "Charline", "Lastname", "Address", "phone", "email", "active", 999),
        ("797", "Name", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("796", "Harold", "Lastname", "Address", "phone", "email", "inactive", -99),
        ("123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("456", "Rachel", "Lastname", "Address", "phone", "email", "inactive", 10),
        ("123", "Name", "Lastname", "Address", "phone", "email", "active", 999),
        ("789", "Marrionberry", "Lastname", "Address", "phone", "email", "active", 0),
        ("345", "Name", "Lastname", "Address", "phone", "email", "active", -10),
        ("0123", "Larry", "Lastname", "Address", "phone", "email", "active", 999),
        ("777", "Name", "Lastname", "Address", "phone", "email", "active", 999)
    ]


def test_integration(_integration_test_filler):
    """ Runs through all operations in basic_operations for a complete test. """
    for customer in _integration_test_filler:
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

    for customer in _integration_test_filler:
        assert bo.search_customer(customer[0])['name'] == customer[1]

    for index, customer in enumerate(_integration_test_filler):
        bo.update_customer_credit(customer[0], index)

        updated_cust = bo.CustomerCredit.select().join(
        bo.Customer).where(bo.Customer.customer_id == customer[0])
        assert updated_cust[0].credit_limit == index

    assert bo.list_active_customers() == 10

    for customer in _integration_test_filler:
        bo.delete_customer(customer[0])

    assert bo.list_active_customers() == 0