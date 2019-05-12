#!/usr/bin/env python3
""" Better performing module #14 """
import numpy as np
import numba
from numba import jit
import datetime

# found = 0
# _2013 = 0
# _2014 = 0
# _2015 = 0
# _2016 = 0
# _2017 = 0
# _2018 = 0

@jit(nopython=True)
def analyze(line, _2013, _2014, _2015, _2016, _2017, _2018, found):
    # global found
    # global _2013 
    # global _2014 
    # global _2015 
    # global _2016 
    # global _2017 
    # global _2018 

    lrow = line.split(',')
    # print(lrow[6])
    if "ao" in lrow[6]:
        found += 1
    # pylint: disable=C0122
    # Less than should be the default comparison operation
    if "2012" < lrow[5][6:]:
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

    return _2013, _2014, _2015, _2016, _2017, _2018, found


def wrapper(filename):
    """ Analyze input filename for some arbitray, but consistent, data """


    found = 0
    _2013 = 0
    _2014 = 0
    _2015 = 0
    _2016 = 0
    _2017 = 0
    _2018 = 0

    start = datetime.datetime.now()

    with open(filename) as csvfile:
        for line in csvfile:
            _2013, _2014, _2015, _2016, _2017, _2018, found = analyze(
                line, _2013, _2014, _2015, _2016, _2017, _2018, found)
        # list(map(analyze, csvfile))
            # lrow = line.split(',')
            # analyze(lrow)

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


if __name__ == "__main__":
    wrapper("data/dataset.csv")
