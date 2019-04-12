#!/usr/bin/env python3
"""
    Queries to test database

"""

import sys
import logging
from datetime import datetime
from peewee import *
from db_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase("database.db")
database.connect()
database.execute_sql("PRAGMA foreign_keys = ON;")


def query_0():
    logger.info("----------------------------------------------------------")
    query = Person.select(Person, Job).join(Job, JOIN.INNER)
    logger.info(query)

    for person in query:
        logger.info(f"Person {person.person_name} had job {person.job.job_name}")


def query_1():
    logger.info("----------------------------------------------------------")
    query = Person.select(Person, Job).join(Job, JOIN.LEFT_OUTER)
    logger.info(query)

    for person in query:
        try:
            logger.info(f"Person {person.person_name} had job {person.job.job_name}")
        except Exception as e:
            logger.info(f"Person {person.person_name} had no job")


def query_2():
    logger.info("----------------------------------------------------------")
    query = (
        Person.select(Person, fn.COUNT(Job.job_name).alias("job_count"))
        .join(Job, JOIN.LEFT_OUTER)
        .group_by(Person)
        .order_by(Person.person_name)
    )
    logger.info(query)

    for person in query:
        logger.info(f"{person.person_name} had {person.job_count} jobs")


def query_3():
    logger.info("----------------------------------------------------------")
    query = Job.select(Job, Department).join(Department, JOIN.INNER)
    logger.info(query)

    for item in query:
        try:
            logger.info(
                f"Job {item.job_name} is part of {item.job_department.department_name} "
            )
        except Exception as ex:
            logger.info(ex)


def query_4():
    logger.info("----------------------------------------------------------")
    query = Job.select()
    for item in query:
        try:
            start_date = datetime.strptime(item.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(item.end_date, "%Y-%m-%d")
            days_held = (end_date - start_date).days
            logger.info(f"Job {item.job_name} was held for {days_held} days")
        except Exception as ex:
            logger.info(ex)


if __name__ == "__main__":
    try:
        [globals()[str("query_" + str(func))]() for func in range(0, 10)]
    except:
        sys.exit(0)
