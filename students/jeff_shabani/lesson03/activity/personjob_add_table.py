#!/usr/bin/env python3
"""
Simple module to add a table to an existing database"""

import logging

from personjob_modeli import *
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


db = SqliteDatabase('personjob.db')
db.connect()
db.execute_sql(('PRAGMA foreign_keys = ON;'))


class BaseModel(Model):
    class Meta:
        database = db


class Department(BaseModel):
    """
    This class defines a department, which maintains details
    of where and for how long a person held a job.
    """

    department_number = CharField(primary_key=False, max_length=4)
    department_name = CharField(max_length=30)
    department_manager = CharField(max_length=30)
    logger.info('Person is linked to Person table')
    person_name = CharField(max_length=30)
    logger.info('Job is linked to job table')
    job_name = CharField(max_length=30)
    job_duration = DecimalField(decimal_places=1, default=0)
    logger.info('Dates for calculating job duration')
    start_date = DateField(formats='YYYY-MM-DD')
    end_date = DateField(formats='YYYY-MM-DD')

def create_table():

    try:
        db.create_tables([Department])
        logger.info('Table added successfully')
    except Exception as e:
        logger.info(f'Table addition failed with error {e}')

JOB_NAME = 0
START_DATE = 1
END_DATE = 2
SALARY = 3
PERSON_EMPLOYED = 4
DEPT_NUM = 5
DEPT_NAME = 6
DEPT_MGR = 7

logger.info('List of employee data tuples to add to department table')
jobs = [
    ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'A100', 'Market Analytics', 'Ashly Lashbrooke'),
    ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew','A101', 'Market Research', 'Dieter Hekking'),
    ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'B200', 'Cyber Security', 'Jans Feldman'),
    ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter', 'C300', 'Finance', 'Karsten Kruse'),
    ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter', 'C301', 'Forecasting', 'Max Rotring')]


def add_records():

    for job in jobs:
        try:
            with database.transaction():
                new_job = Department.create(
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    person_name=job[PERSON_EMPLOYED],
                    department_number = job[DEPT_NUM],
                    department_name = job[DEPT_NAME],
                    department_manager = job[DEPT_MGR],
                    job_duration = 0)
                new_job.save()

        except Exception as e:
            logger.info(f'Error creating = {job[JOB_NAME]}')
            logger.info(e)

db.close()

if __name__ == '__main__':
    create_table()
    add_records()


