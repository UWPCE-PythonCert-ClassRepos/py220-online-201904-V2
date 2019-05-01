"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
import datetime
from peewee import *

LOG_FILE = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

#info and above to log file
FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)

#info and above message at console
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


LOGGER.info('Here we define our data (the schema)')
LOGGER.info('First name and connect to a database (sqlite here)')

LOGGER.info('The next 3 lines of code are the only database specific code')

DATABASE = SqliteDatabase('customer.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

# if you wanted to use heroku postgres:
#
# psycopg2
#
# parse.uses_netloc.append("postgres")
# url = parse.urlparse(os.environ["DATABASE_URL"])
#
# conn = psycopg2.connect(
# database=url.path[1:],
# user=url.username,
# password=url.password,
# host=url.hostname,
# port=url.port
# )
# database = conn.cursor()
#
# Also consider elephantsql.com (be sure to use configparser for PWß)

LOGGER.info('This means we can easily switch to a different database')

LOGGER.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    '''
    This is peewee default
    '''
    class Meta:
        '''
            This is peewee default
        '''
        database = DATABASE

LOGGER.info('By inheritance only we keep our model (almost) technology neutral')

class Customer(BaseModel):
    """
        This class defines Customer, which maintains details of someone
        for whom we want to research for customer data.
    """
    LOGGER.info('Note how we defined the class')
    LOGGER.info('Specify the fields in our model, their lengths and '
                'if mandatory')
    LOGGER.info('Must be a unique identifier for each person')
    customer_id = CharField(primary_key=True, max_length=30)
    customer_name = CharField(max_length=30)
    customer_lastname = CharField(max_length=30)
    home_address = CharField(max_length=40)
    phone_number = CharField(max_length=30)
    email_address = CharField(max_length=40)
    status = CharField(max_length=40)
    credit_limit = DecimalField(max_digits=7, decimal_places=0)


#class PersonNumKey(BaseModel):
#    """
#        This class defines Person, which maintains details of someone
#        for whom we want to research career to date.
#    """
#    logger.info('An alternate Person class')
#    logger.info("Note: no primary key so we're give one 'for free'")
#    person_name = CharField(max_length = 30)
#    lives_in_town = CharField(max_length = 40)
#    nickname = CharField(max_length = 20, null = True)
