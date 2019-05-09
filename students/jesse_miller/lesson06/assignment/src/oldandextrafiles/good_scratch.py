"""
poorly performing, poorly written module

"""

import datetime
import csv
from timeit import timeit
# import cProfile
# import pstats
# import io
from line_profiler import LineProfiler

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
    print(new_ones)
    print(ao_total)
    return start, end, new_ones, ao_total

        # new_ones = []
        # for row in reader:
            # lrow = list(row)
            # if lrow[5] > '00/00/2012':
                # new_ones.append((lrow[5], lrow[0]))


        # year_count = {
            # "2013": 0,
            # "2014": 0,
            # "2015": 0,
            # "2016": 0,
            # "2017": 0,
            # "2018": 0
        # }
#
        # for new in new_ones:
            # if new[0][6:] == '2013':
                # year_count["2013"] += 1
            # if new[0][6:] == '2014':
                # year_count["2014"] += 1
            # if new[0][6:] == '2015':
                # year_count["2015"] += 1
            # if new[0][6:] == '2016':
                # year_count["2016"] += 1
            # if new[0][6:] == '2017':
                # year_count["2017"] += 1
            # if new[0][6:] == '2018':
                # year_count["2018"] += 1
#
        # print(year_count)
#
    # with open(filename) as csvfile:
        # reader = csv.reader(csvfile, delimiter=',', quotechar='"')
#
        # found = 0
#
        # for line in reader:
            # lrow = list(line)
            # if "ao" in line[6]:
                # found += 1
#
        # print(year_count)
#
        # print(f"'ao' was found {found} times")
        # end = datetime.datetime.now()
#
    # return (start, end, year_count, found)
#


# def main():
    # '''
    # Here's where our filename is, it's hard coded at the moment, I'll see about
    # dynamic later.
    # '''
    # filename = "../data/exercise.csv"
    # analyze(filename)
#


if __name__ == "__main__":
    analyze('../data/exercise.csv')

    # pr = cProfile.Profile()
    # s = io.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # pr.enable()

    # main()

    print(timeit("analyze('exercise.csv')", globals=globals(), number=10))

    # pr.disable()
    # pstats.Stats(pr).print_stats()

    lp = LineProfiler()
    lp_wrapper = lp(analyze)
    lp_wrapper("exercise.csv")
    lp.print_stats()
