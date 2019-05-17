'''
Better performing, and hopefully better module.
'''
# pylint: disable=C0103, W0621

import sys
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
    #return start, end, new_ones, ao_total
    print(new_ones)
    print(f"'ao' was found {ao_total} times")
    print(end - start)


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        print('You must pass in a filename')
        sys.exit(1)
    analyze(filename)


    # print(timeit("analyze(filename)", globals=globals(), number=10))

    # lp = LineProfiler()
    # lp_wrapper = lp(analyze)
    # lp_wrapper("exercise.csv")
    # lp.print_stats()
