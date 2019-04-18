#!/usr/bin/env python3
'''
Testing basic operations and database functions
'''
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
