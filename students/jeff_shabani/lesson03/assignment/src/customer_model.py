#!/usr/bin/env python3
"""
    Creates a customer database to be used
    by mulitple functions within the organization.
"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('customers.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
        This class defines customer, which maintains details of someone
        for whom we want to research career to date.
    """
    customerid = CharField(primary_key=False)
    name = CharField(max_length=30)
    lastname = CharField(max_length=30)
    home_address = CharField(max_length=40)
    phone_number = CharField()
    email = CharField(max_length=40, null=True)
    status = CharField(max_length=1, null=True)
    credit_limit = IntegerField(default=0)
    unique_id = AutoField()

def create_table():
    """
    Create new customer table
    :return: New database table
    """
    try:
        database.create_tables([Customer])
        logger.info('Table added successfully')
    except Exception as e:
        logger.info(f'Table addition failed with error {e}')



if __name__ == '__main__':
    create_table()
    database.close()

