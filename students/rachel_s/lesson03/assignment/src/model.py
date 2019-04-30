#!/usr/bin/env python3

'''Sets up customer DB model'''

# Rachel Schirra
# April 13, 2019
# Python 220 Lesson 02

from peewee import *


db = SqliteDatabase('customer.db')


class Customer(Model):
    '''
    Sets up the structure of the customer db
    '''
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
        database = db


db.create_tables([Customer])
