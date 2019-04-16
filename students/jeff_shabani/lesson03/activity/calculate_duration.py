#!/usr/bin/env python3

"""This module calculates the duration that a job
was held.
"""

import logging

from datetime import date, datetime
from peewee import *
from peewee_migrations import *
from personjob_add_table import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SqliteDatabase('personjob.db')
db.connect()
db.execute_sql(('PRAGMA foreign_keys = ON;'))

logger.info('Simple test query')
query = (Department
         .select(Department.start_date, Department.end_date)
         .where(Department.start_date > date(2001, 9, 22)))
# .where(Department.person_name == 'Peter'))
for person in query:
    print(person.start_date - person.end_date)

try:
    update_query = Department.update(job_duration=0)
    update_query.execute()
    logging.info('Job duration updated successfully')
except Exception as e:
    logger.info(f'Duration updated failed with error {e}')

db.close()
