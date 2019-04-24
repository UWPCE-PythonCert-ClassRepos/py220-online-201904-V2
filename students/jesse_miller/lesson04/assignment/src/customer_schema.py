#!/usr/bin/env python3
#pylint: disable=C0103, R0903, C0111 # Honestly I dislike doing this.
'''
Norton Furniture customer database schema
'''
import logging
import peewee
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Connecting to a sqlite.')

database = peewee.SqliteDatabase(config.database)
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(peewee.Model):
    class Meta:
        database = database

class Customer(BaseModel):
    '''
    Customer data fields
    '''
    logger.info('Customer class configuration')
    customer_id = peewee.CharField(primary_key=True, max_length=30)
    '''
    Primary key is true here, because those are unique identifiers
    '''
    first_name = peewee.CharField(max_length=30)
    last_name = peewee.CharField(max_length=30)
    home_address = peewee.CharField(max_length=100)
    phone_number = peewee.CharField(max_length=20)
    email_address = peewee.CharField(max_length=100)
    active_status = peewee.BooleanField()
    credit_limit = peewee.DecimalField(max_digits=10, decimal_places=2)
