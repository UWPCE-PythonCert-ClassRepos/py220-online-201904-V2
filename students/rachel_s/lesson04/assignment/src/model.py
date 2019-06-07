#!/usr/bin/env python3

'''Sets up customer DB model'''

# Rachel Schirra
# June 02, 2019
# Python 220 Lesson 03

from peewee import *


dbase = SqliteDatabase('customer.db')


class Customer(Model):
    '''Sets up the structure of the customer db'''
    Customer_id = CharField()
    Name = CharField()
    Lastname = CharField()
    Home_address = CharField()
    Phone_number = CharField()
    Email_address = CharField()
    Status = CharField()
    Credit_limit = IntegerField()

    class Meta:
        '''This class uses the customer db'''
        database = dbase


dbase.create_tables([Customer])
