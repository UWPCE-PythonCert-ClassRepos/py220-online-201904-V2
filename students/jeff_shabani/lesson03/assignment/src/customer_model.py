#!/usr/bin/env python3
"""
    Creates a customer database to be used
    by mulitple functions within the organization.
"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('customers')

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    """
    Creates basemodel object"""
    class Meta:
        """
        Creates basemodel object"""
        database = DATABASE


class Customer(BaseModel):
    """
        This class defines customer, which maintains details of someone
        for whom we want to research career to date.
    """
    customer_id = CharField(primary_key=False)
    name = CharField(max_length=30)
    lastname = CharField(max_length=30)
    home_address = CharField()
    phone_number = CharField()
    email = CharField()
    status = TextField()
    credit_limit = IntegerField(default=0)
    unique_id = AutoField()


def create_table():
    """
    Create new customer table
    :return: New database table
    """
    # pylint: disable=W0703
    try:
        DATABASE.create_tables([Customer])
        LOGGER.info('Table added successfully')
    except Exception as error:
        LOGGER.info(f'Table addition failed with error {error}')


create_table()
