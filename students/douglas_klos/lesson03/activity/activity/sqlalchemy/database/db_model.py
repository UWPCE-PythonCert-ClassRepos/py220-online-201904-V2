#!/usr/bin/env python3
"""
    Queries to test database

"""
import logging
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey




# Global Variables
SQLITE = "sqlite"
# MYSQL                   = 'mysql'
# POSTGRESQL              = 'postgresql'
# MICROSOFT_SQL_SERVER    = 'mssqlserver'

# Table Names
PEOPLE = "people"
JOB = "job"
DEPARTMENT = "department"


class MyDatabase:

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("One off program to build the classes from the model in the database")

    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: "sqlite:///{DB}",
        # MYSQL: 'mysql://scott:tiger@localhost/{DB}',
        # POSTGRESQL: 'postgresql://scott:tiger@localhost/{DB}',
        # MICROSOFT_SQL_SERVER: 'mssql+pymssql://scott:tiger@hostname:port/{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username="", password="", dbname=""):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(engine_url)
            # print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        people = Table(
            PEOPLE,
            metadata,
            Column("person_name", String, primary_key=True),
            Column("lives_in_town", String),
            Column("nickname", String),
        )

        department = Table(
            DEPARTMENT,
            metadata,
            Column("number", String, primary_key=True),
            Column("name", String),
            Column("manager", String, ForeignKey("people.person_name")),
        )

        job = Table(
            JOB,
            metadata,
            Column("job_name", String, primary_key=True),
            Column("start_date", String),
            Column("end_date", String),
            Column("salary", String),
            Column("person_employed", String, ForeignKey("people.person_name")),
            Column("job_department", String, ForeignKey("department.number")),
        )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as ex:
            print("Error occurred during Table creation!")
            print(ex)

    def execute_query(self, query=""):
        if query == "":
            return
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as ex:
                print(ex)

    def print_all_data(self, table="", query=""):
        query = query if query != "" else "SELECT * FROM '{}';".format(table)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as ex:
                print(ex)
            else:
                for row in result:
                    print(row)
                result.close()
        print("\n")

    def insert_people(self):
        PERSON_NAME = 0
        LIVES_IN_TOWN = 1
        NICKNAME = 2

        people = [
            ("Andrew", "Sumner", "Andy"),
            ("Peter", "Seattle", None),
            ("Susan", "Boston", "Beannie"),
            ("Pam", "Coventry", "PJ"),
            ("Steven", "Colchester", None),
            ("Fred", "Seattle", "Fearless"),
        ]

        for person in people:
            try:
                query = (
                    f"INSERT INTO {PEOPLE}(person_name, lives_in_town, nickname) "
                    f"VALUES ("
                    f"'{person[PERSON_NAME]}', "
                    f"'{person[LIVES_IN_TOWN]}', "
                    f"'{person[NICKNAME]}') "
                )
                self.execute_query(query)
                self.print_all_data(PEOPLE)
                self.logger.info(f"{person[PERSON_NAME]} added to database")
            except Exception as ex:
                self.logger.info(f"Error creating = {person[PERSON_NAME]}")
                self.logger.info(ex)

    def insert_departments(self):
        DEPARTMENT_NUMBER = 0
        DEPARTMENT_NAME = 1
        DEPARTMENT_MANAGER = 2

        departments = [
            ("DEVS", "Development", "Steven"),
            ("PROD", "Production", "Fred"),
            ("RnD0", "Research", "Peter"),
        ]

        for department in departments:
            try:
                query = (
                    f"INSERT INTO {DEPARTMENT}(number, name, manager) "
                    f"VALUES ("
                    f"'{department[DEPARTMENT_NUMBER]}', "
                    f"'{department[DEPARTMENT_NAME]}', "
                    f"'{department[DEPARTMENT_MANAGER]}') "
                )
                self.execute_query(query)
                self.print_all_data(DEPARTMENT)
                self.logger.info(f"{department[DEPARTMENT_NAME]} added to database")
            except Exception as ex:
                self.logger.info(f"Error creating = {department[DEPARTMENT_NAME]}")
                self.logger.info(ex)

    def insert_jobs(self):
        JOB_NAME = 0
        START_DATE = 1
        END_DATE = 2
        SALARY = 3
        PERSON_EMPLOYED = 4
        PART_OF_DEPARTMENT = 5

        jobs = [
            ("Analyst", "2001-09-22", "2003-01-30", 65500, "Andrew", "RnD0"),
            ("Senior analyst", "2003-02-01", "2006-10-22", 70000, "Andrew", "DEVS"),
            (
                "Senior business analyst",
                "2006-10-23",
                "2016-12-24",
                80000,
                "Andrew",
                "PROD",
            ),
            ("Admin supervisor", "2012-10-01", "2014-11-10", 45900, "Peter", "DEVS"),
            ("Admin manager", "2014-11-14", "2018-01-05", 45900, "Peter", "DEVS"),
        ]

        for job in jobs:
            try:
                query = (
                    f"INSERT INTO {JOB}("
                    f"job_name, "
                    f"start_date, "
                    f"end_date, "
                    f"salary, "
                    f"person_employed, "
                    f"job_department) "
                    f"VALUES ("
                    f"'{job[JOB_NAME]}', "
                    f"'{job[START_DATE]}', "
                    f"'{job[END_DATE]}', "
                    f"'{job[SALARY]}', "
                    f"'{job[PERSON_EMPLOYED]}', "
                    f"'{job[PART_OF_DEPARTMENT]}') "
                )
                self.execute_query(query)
                self.print_all_data(DEPARTMENT)
                self.logger.info(f"{job[JOB_NAME]} added to database")
            except Exception as ex:
                self.logger.info(f"Error creating = {job[JOB_NAME]}")
                self.logger.info(ex)


    def query_db(self, query):
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
