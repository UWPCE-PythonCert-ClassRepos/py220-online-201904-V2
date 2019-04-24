#!/usr/bin/env python3
'''
Testing basic operations and database functions
'''
# pylint: disable-all
import peewee
import unittest.mock
import pytest
import customer_schema as cs
import basic_operations as bops
import customer_creation as cc

customer1 = {'customer_id': '1',
             'first_name': 'Ann',
             'last_name': 'Wilson',
             'home_address': '506 2nd Ave, Seattle, 98104',
             'phone_number': '206-624-0414',
             'email_address': 'awilson@hotmail.com',
             'active_status': True,
             'credit_limit': 100.00}

customer2 = {'customer_id': '2',
             'first_name': 'Kelly',
             'last_name': 'Deal',
             'home_address': '505 2nd Ave, Seattle, 98104',
             'phone_number': '206-635-2732',
             'email_address': 'kdeal@aol.com',
             'active_status': False,
             'credit_limit': 50.00}

customer3 = {'customer_id': '3',
             'first_name': 'Nancy',
             'last_name': 'Wilson',
             'home_address': '506 2nd Ave, Seattle, 98104',
             'phone_number': '206-624-0414',
             'email_address': 'nwilson@hotmail.com',
             'active_status': True,
             'credit_limit': 100.00}

customer4 = {'customer_id': '4',
             'first_name': 'Kim',
             'last_name': 'Deal',
             'home_address': '505 2nd Ave, Seattle, 98104',
             'phone_number': '206-635-2732',
             'email_address': 'kideal@aol.com',
             'active_status': False,
             'credit_limit': 50.00}

customer5 = {'customer_id': '5',
             'first_name': 'Sean',
             'last_name': 'Ysult',
             'home_address': '506 2nd Ave, Seattle, 98104',
             'phone_number': '206-614-6372',
             'email_address': 'sysult@aol.com',
             'active_status': False,
             'credit_limit': 50.00}


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
    cc.main()


def test_add_customers():
    create_empty_database()
    bops.add_customer(**customer1)
    bops.add_customer(**customer2)

    test_customer1 = cs.Customer.get(cs.Customer.customer_id == '1')
    assert test_customer1.first_name == customer1['first_name']
    assert test_customer1.last_name == customer1['last_name']

    test_customer2 = cs.Customer.get(cs.Customer.customer_id == '2')
    assert test_customer2.first_name == customer2['first_name']
    assert test_customer2.last_name == customer2['last_name']

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


def test_customer_search():
    create_sample_database()

    test_customer = bops.search_customer('3')
    assert test_customer['email_address'] == customer3['email_address']
    clear_database()


def test_search_customer_missing():
    create_sample_database()

    assert bops.search_customer('8') == dict()
    clear_database()


def test_update_credit():
    create_sample_database()

    bops.update_customer_credit('1', 25500)
    cust_update = cs.Customer.get(cs.Customer.customer_id == 1)
    assert cust_update.credit_limit == 25500
    clear_database()


def test_update_credit_none():
    create_sample_database()

    with pytest.raises(peewee.DoesNotExist):
        bops.update_customer_credit('44', 5000)

    clear_database()


def test_list_customers():
    create_sample_database()
    assert bops.list_active_customers() == 2
    clear_database()


def test_list_customers_none():
    create_empty_database()
    assert bops.list_active_customers() == 0
    clear_database()


def test_csv_db():
    cs.database.create_tables([cs.Customer])
    bops.import_cust_file('test_customer.csv')
    assert 'Import committed'
    assert test_csv_db
    cs.database.drop_tables([cs.Customer])


def test_output_cust():
    cs.database.create_tables([cs.Customer])
    bops.import_cust_file('test_customer.csv')
    bops.output_cust()
    assert 'Bashirian'
    cs.database.drop_tables([cs.Customer])


def test_all():
    '''
    Okay, this one I'm commenting.  I will be populating a DB and testing all
    the functions against an integrated system.  Wish me luck
    '''
    create_empty_database()

    bops.add_customer(**customer1)
    bops.add_customer(**customer2)
    bops.add_customer(**customer3)
    bops.add_customer(**customer4)

    '''
    Here, we will delete Kim Deal.  Which is a shame, I loved The Breeders when
    I was a kid
    '''
    bops.delete_customer(customer4['customer_id'])

    '''
    Now let's delete someone not there
    '''
    bops.delete_customer(customer5['customer_id'])
    assert 'ERROR'

    '''
    Now, let's give the guitarist from Heart a lot more money, then check if
    it worked.
    '''
    bops.update_customer_credit('3', 20000)

    nancy_update = cs.Customer.get(cs.Customer.customer_id == 3)
    assert nancy_update.credit_limit == 20000

    '''
    Here, we're going to find Nancy's sister Ann.
    '''
    ann_search = bops.search_customer(customer1['customer_id'])
    assert ann_search['first_name'] == customer1['first_name']

    '''
    Last, we list the active customers
    '''
    assert bops.list_active_customers() == 2


    # def test_init():
        # '''
        # This, is because I'm curious and I have a few minutes
        # '''
        # with mock.patch.object(module, 'main', return_value=42):
            # with mock.patch.object(module, '__name__', '__main__'):
                # with mock.patch.object(module.sys,'exit') as mock_exit:
                    # module.init()
#
                    # assert mock_exit.call_args[0][0] == 42
#
#  Yeah, this doesn't work as I want
