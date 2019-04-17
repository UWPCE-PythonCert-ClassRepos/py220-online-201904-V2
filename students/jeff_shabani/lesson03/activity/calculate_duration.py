#!/usr/bin/env python3

"""This module calculates the duration that a job
was held.
"""

import logging

from datetime import date, datetime
from peewee import *
# from peewee_migrations import *
from personjob_add_table import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase('personjob.db')
db.connect()
db.execute_sql(('PRAGMA foreign_keys = ON;'))

logger.info('This query should return years in job but currently returns days')
query = (Department
         .select(Department.start_date, Department.end_date))

for person in query:
    print((person.end_date - person.start_date) / 365)

logger.info('This updates job duration field')
try:
    update_query = Department.update(job_duration=Department.end_date - Department.start_date)
    update_query.execute()
    logging.info('Job duration updated successfully')
except Exception as e:
    logger.info(f'Duration updated failed with error {e}')

db.close()
