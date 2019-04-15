#pylint: disable=E0401, R0903
""" SQLAlchemy database hook and class / table definitions for HP Norton """

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


BASE = declarative_base()


class Customer(BASE):
    """
        This class defines a customer for HP Norton.
    """
    __tablename__ = "customer"

    customer_id = Column(String(8), primary_key=True)
    name = Column(String(30))
    last_name = Column(String(30))
    home_address = Column(String(30))
    phone_number = Column(String(30))
    email_address = Column(String(30))
    status = Column(String(30))
    credit_limit = Column(Integer)
