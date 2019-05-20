"""
program to generate one million records
"""
import csv
import uuid
import logging
from datetime import date, timedelta

import random

logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)


CSV_DICT = {}

with open('../data/exercise.csv', 'r', newline='') as csvfile:

    EX_FILE = csv.reader(csvfile)

    N = 1

    for row in EX_FILE:

        CSV_DICT[N] = {'guid': row[0], 'num1': row[1], 'num2': row[2],

                       'num3': row[3], 'num4': row[4], 'date': row[5],

                       'ao': row[6]}

        N += 1



def new_date(rand):

    """Generates random date between 2010-2018 """

    date1 = date(2000, 1, 1)

    new_date_random = date1 + timedelta(rand)

    return new_date_random.strftime("%m/%d/%Y")


def ao_choice(choice):

    """ pick ao or no ao"""

    if choice == 1:
        return 'ao'

    else:

        return ''

LOGGER.info('starting to write file')
for i in range(11, 1000000, 1):
    CSV_DICT[i] = {'guid': uuid.uuid1(), 'num1': 10 + i,

                   'num2': 11 + i, 'num3': 12 + i,

                   'num4': 13 + i,

                   'date': new_date(random.randint(1, 7060)),

                   'ao': ao_choice(random.randint(0, 1))}


with open('../data/exercise2.csv', 'w', newline='') as csvfile:

    NEW_FILE = csv.DictWriter(csvfile, fieldnames=['guid', 'num1', 'num2',

                                                   'num3', 'num4', 'date',

                                                   'ao'])

    for key in CSV_DICT:

        NEW_FILE.writerow(CSV_DICT[key])
LOGGER.info('finished writing file')
