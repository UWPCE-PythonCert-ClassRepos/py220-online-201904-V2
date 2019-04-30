#!/usr/bin/env python3

import sys
from loguru import logger as log

# This allows me to execute the file directly via ./src/database_operations.py,
#   or import it into the main database.py or test files.
#   I'm not sure if this is considered pythonic or proper, however it works.
try:
    import mongodb_conn as mdb
except ModuleNotFoundError:
    import src.mongodb_conn as mdb


def drop_databases():
    log.warning("Dropping databases, lol!")
    mongo = mdb.MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        customers = db['customers']
        log.warning('Dropping "Cusomters"')
        customers.drop()

        rental = db['rental']
        log.warning('Dropping "Rental"')
        rental.drop()

        product = db['product']
        log.warning('Dropping "Product"')
        product.drop()

    log.warning("Purge complete!")


if __name__ == '__main__':
    drop_databases()
