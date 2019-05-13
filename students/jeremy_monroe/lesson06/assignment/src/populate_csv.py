"""
When run this module will populate a csv file with 1,000,000 additional records
using randomly generated data.

Requires Faker as a dependency to genereate random data.
"""

import csv
import uuid
from random import randint
from faker import Faker

FAKE = Faker()

# Just kidding. It will only add 1000 records unless you uncomment the other
# repetitions variable.
# REPETITIONS = 1000
REPETITIONS = 250000
# REPETITIONS = 1000000


def add_records(filename):
    """
    Populates a csv file with random information following the structure of
    exercise.csv.
    """
    new_record_gen = ([index+10, str(uuid.uuid4()), index+10, index+10,
                       generate_random_cc_number(), generate_random_date(),
                       generate_random_sentence()] for index in range(REPETITIONS))

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for _ in range(REPETITIONS):
            writer.writerow(next(new_record_gen))

    # for i in range(10):
    #    print(next(new_record_gen))


def generate_random_sentence():
    """ Returns a random sentence """
    return FAKE.sentence(nb_words=10, variable_nb_words=True,
                         ext_word_list=None)


def generate_random_cc_number():
    """ Returns a random cc number """
    return FAKE.credit_card_number(card_type=None)


def generate_random_date():
    """ Generates and returns a random date between the years 1700 and 2300 """
    random_str_time = '{}/{}/{}'.format(str(randint(1, 12)).zfill(2),
                                        str(randint(1, 31)).zfill(2),
                                        randint(1700, 2300))

    return random_str_time


if __name__ == "__main__":
    FILENAME = "data/exercise.csv"
    add_records(FILENAME)
