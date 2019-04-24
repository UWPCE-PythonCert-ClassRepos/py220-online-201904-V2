#!/usr/bin/env python3
#pylint: disable=E0401, W0106
"""
    Imports customer.csv to sqlite database using SQLAlchemy
"""

# Execution time for seeding the database: 333.28548860549927 seconds.
# System: Linux Mint 19, Core i7-6700k at 4.4GHz, 32GB DDR4, NVME2 Drive
# CPU usage was only around 5-6% for the process.

import argparse
import time
from loguru import logger as LOGGER
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db_model as db

# Replace 'from logurur...' with the following to switch to logging package.
# import logging
# logging.basicConfig(level=logging.INFO)
# LOGGER = logging.getLogger(__name__)


def main():
    """Initializes HPNorton database
    """
    start = time.time()
    args = parse_cmd_arguments()
    engine = create_engine("sqlite:///HPNorton.db")

    LOGGER.info("Initializes the HP Norton database from csv")
    LOGGER.info("Adding tables...")

    add_tables(engine)
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # My list comprehension to handle iteration through the csv file
    [
        populate_database(line, session)
        for line in get_line(open_file(args.input))
        if not args.blank
    ]

    session.close()
    # The following line doesn't work properly with loguru.
    #   Using an f-string works with both logging and loguru,
    #   however f-strings throw a pylint error when used with logging.
    # LOGGER.info("Time to init: %s", time.time() - start)
    LOGGER.info(f"Time to init: {time.time() - start}",)



def parse_cmd_arguments():
    """Parses the command line arguments

    Returns:
        ArgumentParser.parse_args
    """
    parser = argparse.ArgumentParser(description="Build HP Norton Database")
    parser.add_argument("-i", "--input", help="input CSV file", required=True)
    parser.add_argument(
        "-b",
        "--blank",
        help="column headers only, no row data",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument("-d", "--debug", help="debugger level", required=False)
    return parser.parse_args()


def add_tables(engine):
    """Adds tables to database
    """
    db.BASE.metadata.create_all(engine)


def populate_database(line, session):
    """Populates database from csv file"

    Arguments:
        filename {string} -- csv file to be read
    """
    customer = line.split(",")
    try:
        new_customer = db.Customer(
            customer_id=customer[0],
            name=customer[1],
            last_name=customer[2],
            home_address=customer[3],
            phone_number=customer[4],
            email_address=customer[5],
            status=customer[6].lower(),
            credit_limit=customer[7],
        )
        session.add(new_customer)
        session.commit()
        LOGGER.info("Adding record for %s", customer[0])
    except IndexError:
        LOGGER.info("End of file")
    except exc.IntegrityError:
        LOGGER.info("Records already in database. Skipping.")
        session.rollback()


def get_line(lines):
    """Generator for lines of content from csv file

    Arguments:
        lines {list} -- List of lines containing data from csv file

    Yields:
        string -- CSV string containing information for a single customer.
    """
    for line in lines:
        yield line


def open_file(filename):
    """Opens the file specified from the command line

    Arguments:
        filename {string} -- Name of CSV file to import

    Returns:
        list containing lines of customer data from csv file
    """
    # I'm assuming pythons garbage collection takes care of closing the file.
    with open(filename, "rb") as content:
        next(content)  # Skip first line, it's the column names
        return content.read().decode("utf-8", errors="ignore").split("\n")


if __name__ == "__main__":
    main()
