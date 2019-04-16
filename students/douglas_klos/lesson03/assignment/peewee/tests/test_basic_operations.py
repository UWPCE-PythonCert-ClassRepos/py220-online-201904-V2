#pylint: disable=R0801, E0401, W0401, E0602
"""
    Additional tests for basic_operations.py
"""

import pytest
from peewee import *
import src.basic_operations as l


@pytest.fixture
def _customers():
    """ Customer list for testing """
    return [
        (
            "C000000",
            "Rickey",
            "Shanahan",
            "337 Eichmann Locks",
            "1-615-598-8649 x975",
            "Jessy@myra.net",
            "Active",
            237,
        ),
        (
            "C000001",
            "Shea",
            "Boehm",
            "3343 Sallie Gateway",
            "508.104.0644 x4976",
            "Alexander.Weber@monroe.com",
            "Inactive",
            461,
        ),
        (
            "C000002",
            "Blanca",
            "Bashirian",
            "0193 Malvina Lake",
            "(240)014-9496 x08349",
            "Joana_Nienow@guy.org",
            "Active",
            689,
        ),
        (
            "C000003",
            "Elfrieda",
            "Skiles",
            "3180 Mose Row",
            "(839)825-0058",
            "Mylene_Smitham@hannah.co.uk",
            "Active",
            90,
        ),
        (
            "C000004",
            "Mittie",
            "Turner",
            "996 Lorenza Points",
            "1-324-023-8861 x025",
            "Clair_Bergstrom@rylan.io",
            "Active",
            565,
        ),
        (
            "C000005",
            "Nicole",
            "Wisozk",
            "0170 Kuphal Knoll",
            "(731)775-3683 x45318",
            "Hudson.Witting@mia.us",
            "Active",
            244,
        ),
        (
            "C000006",
            "Danika",
            "Bechtelar",
            "5067 Goyette Place",
            "503-011-7566 x19729",
            "Wyatt.Hodkiewicz@wyatt.net",
            "Inactive",
            663,
        ),
        (
            "C000007",
            "Elbert",
            "Abbott",
            "36531 Bergstrom Circle",
            "(223)402-1096",
            "Isabelle_Rogahn@isac.biz",
            "Inactive",
            480,
        ),
        (
            "C000008",
            "Faye",
            "Gusikowski",
            "329 Maye Wall",
            "201.358.6143",
            "Lelia_Wunsch@maximo.biz",
            "active",
            222,
        ),
    ]


def test_add_customer(_customers):
    """test add customer
    """
    for customer in _customers:

        with pytest.raises(DoesNotExist):
            query = l.db.Customer.get(l.db.Customer.customer_id == customer[0])

        l.add_customer(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[4],
            customer[5],
            customer[6],
            customer[7],
        )

        query = l.db.Customer.get(l.db.Customer.customer_id == customer[0])
        assert query.customer_id == customer[0]
        assert query.name == customer[1]
        assert query.last_name == customer[2]
        assert query.home_address == customer[3]
        assert query.phone_number == customer[4]
        assert query.email_address == customer[5]
        assert query.status == customer[6].lower()
        assert query.credit_limit == customer[7]

    for customer in _customers:
        query = l.db.Customer.delete().where(
            l.db.Customer.customer_id == customer[0]
        )
        query.execute()


def test_search_customer(_customers):
    """test search customer
    """
    for customer in _customers:
        assert l.search_customer(customer[0]) == {}

    for customer in _customers:

        l.add_customer(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[4],
            customer[5],
            customer[6],
            customer[7],
        )

        result = l.search_customer(customer[0])
        assert result["customer_id"] == customer[0]
        assert result["name"] == customer[1]
        assert result["lastname"] == customer[2]
        assert result["home_address"] == customer[3]
        assert result["phone_number"] == customer[4]
        assert result["email"] == customer[5]
        assert result["status"] == customer[6].lower()
        assert result["credit_limit"] == customer[7]

    for customer in _customers:
        query = l.db.Customer.delete().where(
            l.db.Customer.customer_id == customer[0]
        )
        query.execute()


def test_delete_customer(_customers):
    """test delete customer
    """
    for customer in _customers:
        assert l.delete_customer(customer[0]) is False

    for customer in _customers:
        l.add_customer(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[4],
            customer[5],
            customer[6],
            customer[7],
        )

    for customer in _customers:
        assert l.delete_customer(customer[0]) is True


def test_update_customer(_customers):
    """test update customer
    """
    for customer in _customers:
        with pytest.raises(ValueError):
            l.update_customer_credit(customer[0], 1000)

    for customer in _customers:
        l.add_customer(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[4],
            customer[5],
            customer[6],
            customer[7],
        )

    for customer in _customers:
        query = l.db.Customer.get(l.db.Customer.customer_id == customer[0])
        assert query.credit_limit != 1000
        l.update_customer_credit(customer[0], 1000)
        query = l.db.Customer.get(l.db.Customer.customer_id == customer[0])
        assert query.credit_limit == 1000

    for customer in _customers:
        query = l.db.Customer.delete().where(
            l.db.Customer.customer_id == customer[0]
        )
        query.execute()


def test_list_active_customers(_customers):
    """test list active customers
    """
    active = l.list_active_customers()
    assert active == 0

    for customer in _customers:
        l.add_customer(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[4],
            customer[5],
            customer[6],
            customer[7],
        )

    active = l.list_active_customers()
    assert active == 6

    for customer in _customers:
        query = l.db.Customer.delete().where(
            l.db.Customer.customer_id == customer[0]
        )
        query.execute()


def test_add_integrity_error(_customers):
    """Add records already present to throw Integrity Error
    """
    for customer in _customers:
        l.add_customer(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[4],
            customer[5],
            customer[6],
            customer[7],
        )

    with pytest.raises(IntegrityError):
        for customer in _customers:
            l.add_customer(
                customer[0],
                customer[1],
                customer[2],
                customer[3],
                customer[4],
                customer[5],
                customer[6],
                customer[7],
            )

    for customer in _customers:
        query = l.db.Customer.delete().where(
            l.db.Customer.customer_id == customer[0]
        )
        query.execute()
