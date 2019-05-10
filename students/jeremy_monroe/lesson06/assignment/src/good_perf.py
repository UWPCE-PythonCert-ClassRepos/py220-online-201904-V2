"""
poorly performing, poorly written module

"""

from datetime import datetime
import argparse
import logging
import csv


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def parse_cmd_arguments():
    """
    Parses the optional argument passed in at the command line to turn on
    logging to a file.

    Specifically so I can record timing improvements from various parts of my
    code.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-lf', '--log_file', nargs='?',
                        const=False, help='Log file on or off (true || false)')

    log_file_onoff = parser.parse_args()

    if log_file_onoff:
        formatter = logging.Formatter(("\n%(asctime)s %(filename)s:%(lineno)-3d"
                                       " %(levelname)s\n%(message)s"))

        log_file = "good_perf" + datetime.now().strftime("%Y-%m-%d")+'.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        LOGGER.addHandler(file_handler)


def analyze(filename):
    """
    Analyzes a csv file and returns relevant information about said file
    and the amount of time the analyzation took.
    """
    start = datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        reader_gen_end = datetime.now()
        LOGGER.info('Time to generate csv reader: %s',
                    (reader_gen_end - start))

        new_ones = []

        for row in reader:
            lrow = list(row)

            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))
        new_ones_gen_end = datetime.now()
        LOGGER.info('Time to generate new_ones list: %s',
                    (new_ones_gen_end - reader_gen_end))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            if new[0][6:] == '2014':
                year_count["2014"] += 1
            if new[0][6:] == '2015':
                year_count["2015"] += 1
            if new[0][6:] == '2016':
                year_count["2016"] += 1
            if new[0][6:] == '2017':
                year_count["2017"] += 1
            if new[0][6:] == '2018':
                year_count["2018"] += 1
        time_for_year_count = datetime.now()
        LOGGER.info("Time to populate year_count dict: %s",
                    (time_for_year_count - new_ones_gen_end))

        print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        print(f"'ao' was found {found} times")
        end = datetime.now()

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
