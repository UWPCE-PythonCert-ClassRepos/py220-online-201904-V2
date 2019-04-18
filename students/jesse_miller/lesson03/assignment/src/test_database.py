#!/usr/bin/env python3
'''
Testing basic operations and database functions
'''
# pylint: disable-all
import peewee
import pytest
import customer_schema as cs
import basic_operations as bops

customer1 = {"customer_id": "1",
             "first_name": "Ann",
             "last_name": "Wilson",
             "home_address": "506 2nd Ave, Seattle, 98104",
             "phone_number": "206-624-0414",
             "email_address": "awilson@hotmail.com",
             "active_status": True,
             "credit_limit": 100.00}

customer2 = {"customer_id": "2",
             "first_name": "Kelly",
             "last_name": "Deal",
             "home_address": "505 2nd Ave, Seattle, 98104",
             "phone_number": "206-635-2732",
             "email_address": "kdeal@aol.com",
             "active_status": False,
             "credit_limit": 50.00}

customer3 = {"customer_id": "3",
             "first_name": "Nancy",
             "last_name": "Wilson",
             "home_address": "506 2nd Ave, Seattle, 98104",
             "phone_number": "206-624-0414",
             "email_address": "nwilson@hotmail.com",
             "active_status": True,
             "credit_limit": 100.00}

customer4 = {"customer_id": "4",
             "first_name": "Kim",
             "last_name": "Deal",
             "home_address": "505 2nd Ave, Seattle, 98104",
             "phone_number": "206-635-2732",
             "email_address": "kideal@aol.com",
             "active_status": False,
             "credit_limit": 50.00}


def clear_database():
    '''
    Testing clearing the DB
    '''
    cs.database.drop_tables([
        cs.Customer
    ])

    cs.database.close()


def create_empty_database():
    '''
    Testing DB initializtion
    '''
    clear_database()

    cs.database.create_tables([
        cs.Customer
    ])

    cs.database.close()


def test_add_customers():
    create_empty_database()
    bops.add_customer(**customer1)
    bops.add_customer(**customer2)

    test_customer1 = cs.Customer.get(cs.Customer.customer_id == "1")
    assert test_customer1.first_name == customer1["first_name"]
    assert test_customer1.last_name == customer1["last_name"]

    test_customer2 = cs.Customer.get(cs.Customer.customer_id == "2")
    assert test_customer2.first_name == customer2["first_name"]
    assert test_customer2.last_name == customer2["last_name"]

    clear_database()


def test_add_customers_duplicate():
    create_empty_database()
    bops.add_customer(**customer1)

    with pytest.raises(peewee.IntegrityError):
        bops.add_customer(**customer1)

    clear_database()


def create_sample_database():
    clear_database()

    cs.database.create_tables([
        cs.Customer
    ])
    bops.add_customer(**customer1)
    bops.add_customer(**customer2)
    bops.add_customer(**customer3)
    bops.add_customer(**customer4)

    cs.database.close()
