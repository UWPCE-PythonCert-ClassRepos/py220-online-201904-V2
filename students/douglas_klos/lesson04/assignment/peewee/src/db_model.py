# pylint: disable=E0602, E0401, W0401, R0903, C0103
""" Peewee database hook and class / table definitions for HP Norton """

from peewee import *

database = SqliteDatabase("HPNorton.db")
database.connect()
database.execute_sql("PRAGMA foreign_keys = ON;")


class BaseModel(Model):
    """Peewee BaseModel"""

    class Meta:
        """Meta class"""

        database = database


class Customer(BaseModel):
    """
        This class defines a customer for HP Norton.
    """

    customer_id = CharField(primary_key=True, max_length=8)
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=30)
    status = CharField(max_length=8)
    credit_limit = IntegerField()
