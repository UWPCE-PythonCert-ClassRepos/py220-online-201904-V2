import pytest

import basic_operations as l


def test_connect_db():
    value = l.connect_db('customer.db')
    assert value == True


def test_add_customer():
    counter = 0
    counter += l.add_customer("001", "NameOne", "LastnameOne",
                              "AddressOne", "1", "emailOne", "active",
                              1)
    counter += l.add_customer("002", "NameTwo", "LastnameTwo",
                              "AddressTwo", "2", "emailTwo", "active",
                              2)
    counter += l.add_customer("003", "NameThree", "LastnameThree",
                              "AddressThree", "3", "emailThree", 
                              "active", 3)
    assert counter == 3


def test_delete_customer():
    counter = 0
    counter += l.delete_customer('001')
    counter += l.delete_customer('002')
    counter += l.delete_customer('003')
    assert counter == 3


def test_search_customer():
    # Test searching for a customer that isn't in the DB
    assert l.search_customer('001') == {}
    # Add customers back into DB
    l.add_customer("001", "NameOne", "LastnameOne", "AddressOne", "1",
                   "emailOne", "active", 1)
    l.add_customer("002", "NameTwo", "LastnameTwo", "AddressTwo", "2",
                   "emailTwo", "active", 2)
    l.add_customer("003", "NameThree", "LastnameThree", "AddressThree",
                   "3", "emailThree", "active", 3)
    assert l.search_customer('001') == {'name': 'NameOne',
                                        'lastname': 'LastnameOne',
                                        'email': 'emailOne',
                                        'phone_number': '1'}


def test_get_customer():
    temp_cust = l.get_customer('001')
    assert temp_cust.Customer_id == '001'
    assert temp_cust.Name == 'NameOne'
    assert temp_cust.Lastname == 'LastnameOne'
    assert temp_cust.Home_address == 'AddressOne'
    assert temp_cust.Phone_number == '1'
    assert temp_cust.Email_address == 'emailOne'
    assert temp_cust.Credit_limit == 1
    # Remove contents of DB
    l.delete_customer('001')
    l.delete_customer('002')
    l.delete_customer('003')


def test_load_data():
    temp = l.load_data('../tests/fake.csv')
    fake1 = {
        'Id': 'C000000',
        'Name': 'Rickey',
        'Last_name': 'Shanahan',
        'Home_address': '337 Eichmann Locks',
        'Phone_number': '1-615-598-8649 x975',
        'Email_address': 'Jessy@myra.net',
        'Status': 'Active',
        'Credit_limit': '237'
        }
    fake2 = {
        'Id': 'C000001',
        'Name': 'Shea',
        'Last_name': 'Boehm',
        'Home_address': '3343 Sallie Gateway',
        'Phone_number': '508.104.0644 x4976',
        'Email_address': 'Alexander.Weber@monroe.com',
        'Status': 'Inactive',
        'Credit_limit': '461'
        }
    fake3 = {
        'Id': 'C000002',
        'Name': 'Blanca',
        'Last_name': 'Bashirian',
        'Home_address': '0193 Malvina Lake',
        'Phone_number': '(240)014-9496 x08349',
        'Email_address': 'Joana_Nienow@guy.org',
        'Status': 'Active',
        'Credit_limit': '689'
        }
    assert fake1 == temp[0]
    assert fake2 == temp[1]
    assert fake3 == temp[2]


def test_customer_db_imports():
    l.customer_db_import(l.load_data('../tests/fake.csv'))
    temp1 = l.get_customer('C000000')
    assert temp1.Name == 'Rickey'
    assert temp1.Phone_number == '1-615-598-8649 x975'
    assert temp1.Credit_limit == 237
    temp2 = l.get_customer('C000001')
    assert temp2.Lastname == 'Boehm'
    assert temp2.Home_address == '3343 Sallie Gateway'
    assert temp2.Status == 'inactive'
    temp3 = l.get_customer('C000002')
    assert temp3.Name == 'Blanca'
    assert temp3.Phone_number == '(240)014-9496 x08349'


def test_update_customer_credit():
    temp = l.get_customer('C000000')
    assert temp.Credit_limit == 237
    l.update_customer_credit('C000000', 111)
    temp = l.get_customer('C000000')
    assert temp.Credit_limit == 111


def test_list_active_customers():
    assert l.list_active_customers() == 2
    # Clean up
    l.delete_customer('C000000')
    l.delete_customer('C000001')
    l.delete_customer('C000002')
