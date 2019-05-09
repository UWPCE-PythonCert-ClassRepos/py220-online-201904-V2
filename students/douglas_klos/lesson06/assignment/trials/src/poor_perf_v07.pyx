#!/usr/bin/env python3
"""
poorly performing, poorly written module

"""

import datetime
import csv


def analyze(filename):
    
    cdef int found = 0
    cdef int _2013 = 0
    cdef int _2014 = 0
    cdef int _2015 = 0
    cdef int _2016 = 0
    cdef int _2017 = 0
    cdef int _2018 = 0

    start = datetime.datetime.now()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')

        for row in reader:
            lrow = list(row)

            if "ao" in lrow[6]:
                found += 1

            if lrow[5][6:] == "2013":
                _2013 += 1
            elif lrow[5][6:] == "2014":
                _2014 += 1
            elif lrow[5][6:] == "2015":
                _2015 += 1
            elif lrow[5][6:] == "2016":
                _2016 += 1
            elif lrow[5][6:] == "2017":
                _2017 += 1
            elif lrow[5][6:] == "2018":
                _2018 += 1

    print(f"'ao' was found {found} times")
    print(
        f"2013:{_2013}\t"
        f"2014:{_2014}\t"
        f"2015:{_2015}\t"
        f"2016:{_2016}\t"
        f"2017:{_2017}\t"
        f"2018:{_2018}\n"
    )
    end = datetime.datetime.now()
    return (
        start,
        end,
        {
            "2013": _2013,
            "2014": _2014,
            "2015": _2015,
            "2016": _2016,
            "2017": _2017,
            "2018": _2018,
        },
        found,
    )


def main():
    filename = "../data/dataset.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
