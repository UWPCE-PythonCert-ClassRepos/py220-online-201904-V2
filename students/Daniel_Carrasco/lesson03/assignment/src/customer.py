import logging
from peewee import *
import customer_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Customer class')
logger.info('Creating a database using the Customer model')

customer_model.database.create_tables([customer_model.Customer])
customer_model.database.close()
