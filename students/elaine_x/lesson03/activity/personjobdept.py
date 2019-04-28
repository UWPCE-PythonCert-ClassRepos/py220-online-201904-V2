"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)


"""

from personjobdept_model import *
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Person class')
logger.info('Note how I use constants and a list of tuples as a simple schema')
logger.info('Normally you probably will have prompted for this from a user')

PERSON_NAME = 0
LIVES_IN_TOWN = 1
NICKNAME = 2

people = [
    ('Andrew', 'Sumner', 'Andy'),
    ('Peter', 'Seattle', None),
    ('Susan', 'Boston', 'Beannie'),
    ('Pam', 'Coventry', 'PJ'),
    ('Steven', 'Colchester', None),
    ]

logger.info('Creating Person records: iterate through the list of tuples')
logger.info('Prepare to explain any errors with exceptions')
logger.info('and the transaction tells the database to rollback on error')

for person in people:
    try:
        with database.transaction():
            new_person = Person.create(
                    person_name = person[PERSON_NAME],
                    lives_in_town = person[LIVES_IN_TOWN],
                    nickname = person[NICKNAME])
            new_person.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

logger.info('Read and print all Person records we created...')

for person in Person:
    logger.info(f'{person.person_name} lives in {person.lives_in_town} ' +\
        f'and likes to be known as {person.nickname}')






#######################################################################################
logger.info('Working with Job class')

logger.info('Creating Job records: just like Person. We use the foreign key')

JOB_NAME = 0
START_DATE = 1
END_DATE = 2
SALARY = 3
PERSON_EMPLOYED = 4

jobs = [
    ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew'),
    ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew'),
    ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew'),
    ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter'),
    ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter')
    ]

for job in jobs:
    try:
        with database.transaction():
            new_job = Job.create(
                job_name = job[JOB_NAME],
                start_date = job[START_DATE],
                end_date = job[END_DATE],
                salary = job[SALARY],
                person_employed = job[PERSON_EMPLOYED])
            new_job.save()

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

logger.info('Reading and print all Job rows (note the value of person)...')

for job in Job:
    logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')


#############################################################################################
logger.info('Working with Department class')

logger.info('Creating Department records: just like Job. We use the foreign key')

DEPT_NUMBER = 0
DEPT_NAME = 1
DEPT_MANAGER = 2
JOB_HELD = 3

depts = [
    ('A012', 'AAA', 'Bob Smith', 'Analyst'),
    ('A012', 'AAA', 'Bob Smith', 'Senior analyst'),
    ('A022', 'AA2', 'Susan Lee', 'Senior business analyst'),
    ('B011', 'BBB', 'Jane Doe', 'Admin supervisor'),
    ('B012', 'BB2', 'Mary H', 'Admin manager')
    ]

for dept in depts:
    try:
        with database.transaction():
            ajob = Job.get(Job.job_name == dept[JOB_HELD])
            end_date = datetime.datetime.strptime(ajob.end_date, '%Y-%m-%d')
            start_date = datetime.datetime.strptime(ajob.start_date, '%Y-%m-%d')
            logger.info(f"job end date: {end_date} start date: {start_date}")
            logger.info(f"Calc job duration")
            JOB_DURATION = (end_date - start_date).days
            logger.info(f"job duration is: {JOB_DURATION} days")
            new_dept = Department.create(
                dept_number = dept[DEPT_NUMBER],
                dept_name = dept[DEPT_NAME],
                dept_manager = dept[DEPT_MANAGER],
                job_held = dept[JOB_HELD],
                job_duration = JOB_DURATION)
            new_dept.save()

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NUMBER]}')
        logger.info(e)

logger.info('Reading and print all Department rows (note the job held under the department)...')

for dept in Department:
    logger.info(f'{dept.dept_number} : {dept.dept_name} under manager {dept.dept_manager} '
                f'as {dept.job_held} for {dept.job_duration} days')


database.close()
