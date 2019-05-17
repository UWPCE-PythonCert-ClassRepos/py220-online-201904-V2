""" Slightly better written faster module.
"""

from datetime import datetime
from collections import Counter
import argparse
import logging
import csv


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def parse_cmd_arguments():# {{{
    """
    Parses the optional argument passed in at the command line to turn on
    logging to a file.

    Specifically so I can record timing improvements from various parts of my
    code.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-lf', '--logfile', nargs='?',
                        const=False, help='Log file on or off (true || false)')

    log_file_onoff = parser.parse_args()

    if log_file_onoff.logfile:
        formatter = logging.Formatter(("\n%(asctime)s"
                                       " %(filename)s:%(lineno)-3d"
                                       " %(levelname)s\n%(message)s"))

        log_file = "good_perf" + '.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        LOGGER.addHandler(file_handler)# }}}


def analyze(filename):
    """
    Analyzes a csv file and returns relevant information about said file
    and the amount of time the analyzation took.
    """
    start = datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        year_str = "2013 2014 2015 2016 2017 2018"

        year_generator_reduced = (row[5][6:] for row in reader
                                  if row[5][6:] in year_str)
        next(year_generator_reduced)

        year_count = Counter(year_generator_reduced)
        for year in year_str.split():
            if year not in year_count:
                year_count[year] = 0
        print("Year_count:\n{}".format(year_count))

        year_count_timer = datetime.now()
        LOGGER.info('Time to count years: %s',
                    (year_count_timer - start))

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        ao_reduced_generator = ('ao' for row in reader if 'ao' in row[6])
        found = Counter(ao_reduced_generator)['ao']

        print(f"'ao' was found {found} times")
        end = datetime.now()

    LOGGER.info("Time to search for 'ao': %s", (end - year_count_timer))
    LOGGER.info('Total time taken: %s', (end-start))
    return (start, end, year_count, found)


def main():
    """ To be run if __name__ == __main__ """
    parse_cmd_arguments()
    filename = "data/exercise.csv"
    # filename = 'data/test.csv'
    analyze(filename)


if __name__ == "__main__":
    main()
