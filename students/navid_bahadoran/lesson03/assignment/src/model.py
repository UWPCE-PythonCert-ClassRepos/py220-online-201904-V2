# pylint: disable = W0401, R0903, C0103, W1203, W0614, E0602, E0401, R0913
""" Creating Model fro our customer table"""

from peewee import *

DB = SqliteDatabase('HPNorton_test.db', pragmas={'foreign_keys': 1})
DB.connect()


class BaseModel(Model):
    """ This is the base class for our table in database """

    class Meta:
        """ This the Meta class for our base model"""
        database = DB


class Customer(BaseModel):
    """ This is Customer table class"""
    customer_id = CharField(primary_key=True, max_length=8)
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=30)
    status = CharField(max_length=8)
    credit_limit = IntegerField()


# DB.create_tables([Customer])
