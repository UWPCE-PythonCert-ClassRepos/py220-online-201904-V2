#!/usr/bin/env python3

'''
Better performing, still probably poorly written module

'''

# Rachel Schirra
# May 12, 2019
# Python 220 Lesson 06

import datetime
import csv

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # new_ones = []
        # We are reading each row in the reader and appending it to a 
        # list. Why aren't we just looking at the row, checking the 
        # info we need, updating counts as necessary, and then
        # discarding the row?

        # Let's set up the year count before we start reading the CSV.
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for row in reader:
            lrow = list(row)
            year = lrow[5][6:]
            # if lrow[5] > '00/00/2012':
                # Instead of appending the row to a list, let's check
                # the year in place.
                # new_ones.append((lrow[5], lrow[0]))
            if year in year_count.keys():
                year_count[year] += 1

        # for new in new_ones:
        #     if new[0][6:] == '2013':
        #         year_count["2013"] += 1
        #     if new[0][6:] == '2014':
        #         year_count["2014"] += 1
        #     if new[0][6:] == '2015':
        #         year_count["2015"] += 1
        #     if new[0][6:] == '2016':
        #         year_count["2016"] += 1
        #     if new[0][6:] == '2017':
        #         year_count["2017"] += 1
        #     if new[0][6:] == '2018':
        #         year_count["2017"] += 1

        print(year_count)

    # Now we're opening the CSV again and reading it again even though
    # we've already iterated over it one time.
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    filename = "data/out.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
