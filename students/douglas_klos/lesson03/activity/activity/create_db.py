#!/usr/bin/env python3
"""
    Create database examle with Peewee ORM, sqlite and Python
"""

import logging
from db_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("One off program to build the classes from the model in the database")

database.create_tables([Job, Person, Department, PersonNumKey])


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

logger.info("Creating Person records")

for person in people:
    try:
        with database.transaction():
            new_person = Person.create(
                person_name=person[PERSON_NAME],
                lives_in_town=person[LIVES_IN_TOWN],
                nickname=person[NICKNAME],
            )
            new_person.save()
            logger.info(f"{person[PERSON_NAME]} added to database")

    except Exception as ex:
        logger.info(f"Error creating = {person[PERSON_NAME]}")
        logger.info(ex)


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
        with database.transaction():
            new_department = Department.create(
                department_number=department[DEPARTMENT_NUMBER],
                department_name=department[DEPARTMENT_NAME],
                department_manager=department[DEPARTMENT_MANAGER],
            )
            new_department.save()
            logger.info(f"{department[DEPARTMENT_NAME]} added to database")

    except Exception as ex:
        logger.info(f"Error creating = {department[DEPARTMENT_NAME]}")
        logger.info(ex)


JOB_NAME = 0
START_DATE = 1
END_DATE = 2
SALARY = 3
PERSON_EMPLOYED = 4
PART_OF_DEPARTMENT = 5

jobs = [
    ("Analyst", "2001-09-22", "2003-01-30", 65500, "Andrew", "RnD0"),
    ("Senior analyst", "2003-02-01", "2006-10-22", 70000, "Andrew", "DEVS"),
    ("Senior business analyst", "2006-10-23", "2016-12-24", 80000, "Andrew", "PROD"),
    ("Admin supervisor", "2012-10-01", "2014-11-10", 45900, "Peter", "DEVS"),
    ("Admin manager", "2014-11-14", "2018-01-05", 45900, "Peter", "DEVS"),
]

for job in jobs:
    try:
        with database.transaction():
            new_job = Job.create(
                job_name=job[JOB_NAME],
                start_date=job[START_DATE],
                end_date=job[END_DATE],
                salary=job[SALARY],
                person_employed=job[PERSON_EMPLOYED],
                job_department=job[PART_OF_DEPARTMENT],
            )
            new_job.save()
            logger.info(f"{job[JOB_NAME]} added to database")

    except Exception as ex:
        logger.info(f"Error creating = {job[JOB_NAME]}")
        logger.info(ex)


database.close()
