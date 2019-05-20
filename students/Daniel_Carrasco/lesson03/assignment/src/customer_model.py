import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# logger.info('Here we define our data (the schema)')
# logger.info('First name and connect to a database(sqlite here)')

database = SqliteDatabase('customer.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    '''
    Basemodel class
    '''
    class Meta:
        '''
            Meta class
        '''
        database = database

# logger.info('By inheritance only we keep our model technology neutral')


class Customer(BaseModel):
    """
        This class defines Customer, which maintains their details
    """
    # logger.info('Note how we defined the class')
    # logger.info('Specify the fields in our model, their lengths')
    # logger.info('Must be a unique identifier for each person')
    customer_id = CharField(primary_key=True, max_length=30)
    customer_name = CharField(max_length=20)
    customer_lastname = CharField(max_length=20)
    home_address = CharField(max_length=30)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=30)
    status = CharField(max_length=30)
    credit_limit = IntegerField()
