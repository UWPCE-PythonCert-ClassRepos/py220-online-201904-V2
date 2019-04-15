#!/usr/bin/env python3
#pylint: disable=E0401
"""
    Queries to test database

"""
import logging
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData


SQLITE = "sqlite"
CUSTOMER = "customer"


class MyDatabase:
    """SQLAlchemy ORM for HP Norton"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Initialize HP Norton database from CSV useing SQLAlchemy")

    DB_ENGINE = {
        SQLITE: "sqlite:///{DB}",
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, dbname=""):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
        else:
            self.logger.info("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        """Create Customer table
        """
        metadata = MetaData()
        Table(
            CUSTOMER,
            metadata,
            Column("customer_id", String, primary_key=True),
            Column("name", String),
            Column("last_name", String),
            Column("home_address", String),
            Column("phone_number", String),
            Column("email_address", String),
            Column("status", String),
            Column("credit_limit", Integer),
        )
        try:
            metadata.create_all(self.db_engine)
            self.logger.info("Tables created")
        except Exception as ex:
            self.logger.info("Error occurred during Table creation!")
            self.logger.info(ex)

    def insert_people(self, filename):
        """Insert customers from specified csv file

        Arguments:
            filename {string} -- CSV file to load data from
        """
        with open(filename, "rb") as content:
            next(content)  # Skip first line, it's the column names
            lines = content.read().decode("utf-8", errors="ignore").split("\n")
            for line in lines:
                customer = line.split(",")
                try:
                    query = (
                        f'INSERT INTO {CUSTOMER}(customer_id, name, last_name, '
                        f'home_address, phone_number, email_address, '
                        f'status, credit_limit) VALUES ('
                        f'"{customer[0]}", '
                        f'"{customer[1]}", '
                        f'"{customer[2]}", '
                        f'"{customer[3]}", '
                        f'"{customer[4]}", '
                        f'"{customer[5]}", '
                        f'"{customer[6]}", '
                        f'"{customer[7]}") '
                    )
                    self.execute_query(query)
                    # self.print_all_data(CUSTOMER)
                    self.logger.info("%s added to database", customer[0])
                except IndexError:
                    self.logger.info("End of file")

    def execute_query(self, query=""):
        """Execute query
        """
        if query == "":
            return
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as ex:
                self.logger.info(ex)

    def query_db(self, query):
        """Runs a query and returns a string with the result

        Arguments:
            query {string} -- query to orun

        Returns:
            string -- result of the query
        """
        return_result = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as ex:
                print(ex)
            else:
                for row in result:
                    return_result.append(row)
                result.close()
        return return_result
