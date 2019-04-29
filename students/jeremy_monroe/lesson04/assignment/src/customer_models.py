""" This is where my Customer model is defined. """

import logging
from datetime import datetime
# from peewee import *
from peewee import SqliteDatabase, Model, CharField, IntegerField
from peewee import ForeignKeyField


log_format = ("\n%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s"
        "\n%(message)s")
formatter = logging.Formatter(log_format)
log_file = datetime.now().strftime("%Y-%m-%d")+'.log'

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(console_handler)
LOGGER.addHandler(file_handler)

LOGGER.info("Ok, defining my base model and customer model")

DB = SqliteDatabase('customer.db')
DB.connect()
DB.execute_sql('PRAGMA foreign_keys= ON;')


class BaseModel(Model):
    """ The base model for my future models. """
    class Meta:
        """ Just here for functionality. """
        database = DB


class Customer(BaseModel):
    """ A class to model a Customer's information in a database. """
    customer_id = CharField(primary_key=True)
    name = CharField(max_length=30)
    lastname = CharField(max_length=30)
    home_address = CharField()
    phone_number = CharField(max_length=11)
    email_address = CharField(max_length=30)


class CustomerCredit(BaseModel):
    """ A class to store a customers credit limit. """
    customer = ForeignKeyField(Customer, primary_key=True)
    credit_limit = IntegerField()


class CustomerStatus(BaseModel):
    """ A class to keep track whether customer's are active or inactive. """
    customer = ForeignKeyField(Customer, primary_key=True)
    status = CharField(max_length=8)


# Customer.create_table()
DB.create_tables([Customer, CustomerCredit, CustomerStatus])
