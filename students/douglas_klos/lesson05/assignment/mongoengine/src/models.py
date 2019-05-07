"""Collection models for HPNorton MongoEngine interface
"""

import mongoengine


class Customers(mongoengine.Document):
    """Customer collection model
    """

    user_id = mongoengine.StringField(
        required=True, max_length=7, unique=True
    )
    name = mongoengine.StringField(
        required=True, max_length=60
    )
    address = mongoengine.StringField(
        required=True, max_length=60
    )
    zip_code = mongoengine.StringField(
        required=True, max_length=10
    )
    phone_number = mongoengine.StringField(
        required=True, max_length=20
    )
    email = mongoengine.StringField(
        required=True, max_length=60
    )


class Product(mongoengine.Document):
    """Product collection model
    """

    product_id = mongoengine.StringField(
        required=True, max_length=60, unique=True
    )
    description = mongoengine.StringField(
        required=True, max_length=60
    )
    product_type = mongoengine.StringField(
        required=True, max_length=60
    )
    quantity_available = mongoengine.IntField()


class Rental(mongoengine.Document):
    """Rental collection model
    """

    product_id = mongoengine.StringField(
        required=True, max_length=60
    )
    user_id = mongoengine.StringField(
        required=True, max_length=60, unique_with="product_id"
    )
