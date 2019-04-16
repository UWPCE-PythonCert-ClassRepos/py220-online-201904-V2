# pylint: disable=C0111, R0801
"""
    Autograde Lesson 3 assignment
    Run pytest
    Run coverage and linitng using standard batch file
    Student should submit an empty database

"""


import pytest
import src.basic_operations as l


@pytest.fixture
def _add_customers():
    return [
        ("123", "Name", "Lastname", "Address", "cell", "email", "active", 999),
        ("234", "Name", "Lastname", "Address", "cell", "email", "inactive", 5),
        ("345", "Name", "Lastname", "Address", "cell", "email", "active", 999),
        ("456", "Name", "Lastname", "Address", "cell", "email", "active", 0),
        ("567", "Name", "Lastname", "Address", "cell", "email", "active", -10),
        ("678", "Name", "Lastname", "Address", "cell", "email", "active", 999),
        ("789", "Name", "Lastname", "Address", "cell", "email", "active", 999),
    ]


@pytest.fixture
def _search_customers():  # needs to del with database
    return [
        [
            ("998", "Name", "Last", "Address", "cell", "email", "active", 999),
            ("997", "Name", "Last", "Address", "cell", "email", "inactive", 10),
        ],
        ("998", "000"),
    ]


@pytest.fixture
def _delete_customers():  # needs to del with database
    return [
        ("898", "Name", "Lastname", "Address", "cell", "email", "active", 999),
        ("897", "Name", "Lastname", "Address", "cell", "email", "inactive", 0),
    ]


@pytest.fixture
def _update_customer_credit():  # needs to del with database
    return [
        ("798", "Name", "Lastname", "Address", "cell", "email", "active", 999),
        ("797", "Name", "Lastname", "Address", "cell", "email", "inactive", 10),
        ("796", "Name", "Lastname", "Address", "cell", "email", "inactive", -9),
    ]


@pytest.fixture
def _list_active_customers():
    return [
        ("598", "Name", "Lastname", "Address", "cell", "email", "active", 999),
        ("597", "Name", "Lastname", "Address", "cell", "email", "inactive", 10),
        ("596", "Name", "Lastname", "Address", "cell", "email", "inactive", 99),
        ("595", "Name", "Lastname", "Address", "cell", "email", "active", 999),
        ("594", "Name", "Lastname", "Address", "cell", "email", "active", 10),
        ("593", "Name", "Lastname", "Address", "cell", "email", "active", 99),
    ]


def test_list_active_customers(_list_active_customers):
    """Test list active customers
    """
    for customer in _list_active_customers:
        l.add_customer(customer[0], customer[1], customer[2],
                       customer[3], customer[4], customer[5],
                       customer[6], customer[7],
                       )
    actives = l.list_active_customers()
    assert actives == 4

    for customer in _list_active_customers:
        l.delete_customer(customer[0])


def test_add_customer(_add_customers):
    """Test add customer
    """
    for customer in _add_customers:
        l.add_customer(customer[0], customer[1], customer[2],
                       customer[3], customer[4], customer[5],
                       customer[6], customer[7]
                       )
        added = l.search_customer(customer[0])
        assert added["name"] == customer[1]
        assert added["lastname"] == customer[2]
        assert added["email"] == customer[5]
        assert added["phone_number"] == customer[4]

    for customer in _add_customers:
        l.delete_customer(customer[0])


def test_search_customer(_search_customers):
    """Test search
    """
    for customer in _search_customers[0]:
        l.add_customer(customer[0], customer[1], customer[2],
                       customer[3], customer[4], customer[5],
                       customer[6], customer[7],
                       )
    result = l.search_customer(_search_customers[1][1])
    assert result == {}

    result = l.search_customer(_search_customers[1][0])
    assert result["name"] == _search_customers[0][1][1]
    assert result["lastname"] == _search_customers[0][1][2]
    assert result["email"] == _search_customers[0][1][5]
    assert result["phone_number"] == _search_customers[0][1][4]

    for customer in _search_customers[0]:
        print(customer[0])
        l.delete_customer(customer[0])


def test_delete_customer(_delete_customers):
    """Test delete customer
    """
    for customer in _delete_customers:
        l.add_customer(customer[0], customer[1], customer[2],
                       customer[3], customer[4], customer[5],
                       customer[6], customer[7],
                       )
        response = l.delete_customer(customer[0])
        assert response is True

        deleted = l.search_customer(customer[0])
        assert deleted == {}


def test_update_customer_credit(_update_customer_credit):
    """Test update credit limit
    """
    for customer in _update_customer_credit:
        l.add_customer(customer[0], customer[1], customer[2],
                       customer[3], customer[4], customer[5],
                       customer[6], customer[7],
                       )
    l.update_customer_credit("798", 0)
    l.update_customer_credit("797", 1000)
    l.update_customer_credit("797", -42)
    l.update_customer_credit("796", 500)

    with pytest.raises(ValueError) as excinfo:
        l.update_customer_credit("00100", 1000)  # error
        assert "NoCustomer" in str(excinfo.value)

    for customer in _update_customer_credit:
        l.delete_customer(customer[0])
