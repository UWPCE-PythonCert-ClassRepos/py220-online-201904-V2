"""
    Create database example with Peewee ORM, sqlite and Python
"""

import logging
import customer_model as cm

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


LOGGER.info(

    'One off program to build the classes from the model in the database')
cm.database.create_tables([cm.Customer])
cm.database.close()
