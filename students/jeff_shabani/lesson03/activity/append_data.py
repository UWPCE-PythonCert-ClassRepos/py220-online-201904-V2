#!/usr/bin/env python3

"""
A module that queries the job table and appends those same records
to the Department table.
"""

import logging

from personjob_add_table import Department
from personjob_modeli import *
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase('personjob.db')
db.connect()
db.execute_sql(('PRAGMA foreign_keys = ON;'))

JOB_NAME = 0
START_DATE = 1
END_DATE = 2
SALARY = 3
PERSON_EMPLOYED = 4
DEPT_NUM = 5
DEPT_NAME = 6
DEPT_MGR = 7

jobs = [
    ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'A100', 'Market Analytics', 'Ashly Lashbrooke'),
    ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew','A101', 'Market Research', 'Dieter Hekking'),
    ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'B200', 'Cyber Security', 'Jans Feldman'),
    ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter', 'C300', 'Finance', 'Karsten Kruse'),
    ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter', 'C301', 'Forecasting', 'Max Rotring')]

# logging.info('Create tuple list of jobs fields')
# logging.info('This works for getting a list but not for adding data to dept')
# query =Job.select().tuples()
# jobs = []
# for row in query:
#     jobs.append(row)

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
