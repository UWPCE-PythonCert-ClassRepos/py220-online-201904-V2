#!/usr/bin/env python3

"""This module prints out a person's job history
based on user-inputted name.

"""
from logging import *
from personjob_add_table import *

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)

select_fields = (Department.person_name, Department.department_name, Department.job_name,
                 Department.start_date, Department.end_date)

query = (Department
         .select(Department.person_name, Department.department_name, Department.job_name,
                 Department.start_date, Department.end_date)
         .where(Department.person_name == input('Please enter a name:')))

for person in query:
    print(f'{person.person_name} worked in {person.department_name} as a/an {person.job_name} '
          f'from {person.start_date} until {person.end_date}.')

db.close()
