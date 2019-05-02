from mongoengine import *


class Customers(Document):
    user_id = StringField(required=True, max_length=7, unique=True)
    name = StringField(required=True, max_length=60)
    address = StringField(required=True, max_length=60)
    zip_code = StringField(required=True, max_length=10)
    phone_number = StringField(required=True, max_length=20)
    email = StringField(required=True, max_length=60)


class Product(Document):
    product_id = StringField(required=True, max_length=60, unique=True)
    description = StringField(required=True, max_length=60)
    product_type = StringField(required=True, max_length=60)
    quantity_available = IntField()


class Rental(Document):
    product_id = StringField(required=True, max_length=60)
    user_id = StringField(required=True, max_length=60, unique_with='product_id')
