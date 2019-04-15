#!/usr/bin/env python3
"""Initialize HP Norton database with SQLAlchemy"""

# Execution time for seeding the database: 304 seconds.
# System: Linux Mint 19, Core i7-6700k at 4.4GHz, 32GB DDR4, NVME2 Drive
# CPU usage was only around 5-6% for the process.


import argparse
import time
import logging
import db_model as db


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
CUSTOMER = "customer"


def main():
    """HP Norton initialize database with SQLAlchemy
    """
    start = time.time()
    args = parse_cmd_arguments()
    LOGGER.info("Initializes the HP Norton database from csv")
    dbms = db.MyDatabase(db.SQLITE, dbname='SQLAlchemy.db')
    LOGGER.info("Adding tables...")
    dbms.create_db_tables()
    dbms.insert_people(args.input)
    LOGGER.info("Time to init: %s", time.time() - start)



def parse_cmd_arguments():
    """Parses the command line arguments

    Returns:
        ArgumentParser.parse_args
    """
    parser = argparse.ArgumentParser(description="Build HP Norton Database")
    parser.add_argument("-i", "--input", help="input CSV file", required=True)
    parser.add_argument("-d", "--debug", help="debugger level", required=False)
    return parser.parse_args()


if __name__ == "__main__":
    main()
