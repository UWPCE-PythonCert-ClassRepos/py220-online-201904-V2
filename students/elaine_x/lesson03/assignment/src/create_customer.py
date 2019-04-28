"""
    Create database examle with Peewee ORM, sqlite and Python

"""
import logging
from customer_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


LOGGER.info('One off program to build the classes from the model in '
            'the database')

DATABASE.create_tables([Customer])
        #PersonNumKey

DATABASE.close()
