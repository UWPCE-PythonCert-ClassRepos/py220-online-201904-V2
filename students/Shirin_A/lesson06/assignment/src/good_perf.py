"""
good performing written module
"""

import datetime

import csv

import logging

from timeit import timeit as timer


logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# pylint: disable=C0303, W0641, C0330

def analyze(filename):

    """Analyzes file for certain years and letters"""

    start = datetime.datetime.now()

    with open(filename) as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        year_count = {"2013": 0, "2014": 0, "2015": 0, "2016": 0, "2017": 0,

                      "2018": 0}

        found = [0]

        LOGGER.info('Run time for counting years and filtering for "ao":'

                    ' %s sec', timer(

        '''for row in reader:

            if "ao" in row[6]:
                found[0] += 1              
            try:
                year_count[row[5][6:]] += 1

            except KeyError:

                continue

        ''', globals=locals(), number=1))

        print(year_count)

        print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return (start, end, year_count, found)



def main():

    """Calls and runs analyze()"""

    LOGGER.info('main() run time: %s sec', timer(

        'filename = "../data/exercise.csv"\nanalyze(filename)', globals=globals(),

        number=1))



if __name__ == "__main__":

    LOGGER.info('Program run time: %s sec', timer('main()', globals=globals(),

                                                  number=1))
