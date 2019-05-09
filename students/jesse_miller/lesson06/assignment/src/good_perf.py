'''
Better performing, and hopefully better module.
'''

import datetime
import csv
# from timeit import timeit
# from line_profiler import LineProfiler


def analyze(filename):
    '''
    This analyzes the file for parsing via the below rules.
    '''
    start = datetime.datetime.now()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None)  # Skipping the header row.

        new_ones = {}
        ao_total = 0


        for row in reader:
            if '2012' < row[5][-4:] < '2019':
                new_ones[row[5][-4:]] = new_ones.get(row[5][-4:], 0) + 1

            if 'ao' in row[6]:
                ao_total += 1

        end = datetime.datetime.now()
    return start, end, new_ones, ao_total


if __name__ == "__main__":
    analyze('../data/exercise.csv')


    # print(timeit("analyze('exercise.csv')", globals=globals(), number=10))

    # lp = LineProfiler()
    # lp_wrapper = lp(analyze)
    # lp_wrapper("exercise.csv")
    # lp.print_stats()
