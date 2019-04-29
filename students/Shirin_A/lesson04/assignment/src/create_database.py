"""
    Create database example with Peewee ORM, sqlite and Python
"""

import logging
import customer_model as cm


def main():
    """Create customer table"""
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


LOGGER.info('Creating a database using the customer model')
cm.database.create_tables([cm.Customer])
cm.database.close()
