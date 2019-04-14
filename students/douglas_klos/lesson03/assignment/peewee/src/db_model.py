from peewee import *

database = SqliteDatabase("HPNorton.db")
database.connect()
database.execute_sql("PRAGMA foreign_keys = ON;")


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    """
        This class defines a customer for HP Norton.
    """

    customer_id = CharField(primary_key=True, max_length=12)
    name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    home_address = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=30)
    status = CharField(max_length=30)
    credit_limit = CharField(max_length=30)
