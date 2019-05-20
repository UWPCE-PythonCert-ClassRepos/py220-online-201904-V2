#!/usr/bin/env python3
""" Better performing module #14 """

import re
import datetime

FOUND = 0
_2013 = 0
_2014 = 0
_2015 = 0
_2016 = 0
_2017 = 0
_2018 = 0


def analyze(lrow):
    """ Analyze input filename for some arbitray, but consistent, data """
    #pylint: disable=W0603
    global FOUND
    global _2013
    global _2014
    global _2015
    global _2016
    global _2017
    global _2018

    if re.search(r'ao', lrow[6]):
        FOUND += 1

    if re.search(r'([2]{1}[0]{1}[1]{1}[3-8]{1})', lrow[5]):
        if re.search(r'([2]{1}[0-1]{2}[3]{1})', lrow[5]):
            _2013 += 1
        elif re.search(r'([2]{1}[0-1]{2}[4]{1})', lrow[5]):
            _2014 += 1
        elif re.search(r'([2]{1}[0-1]{2}[5]{1})', lrow[5]):
            _2015 += 1
        elif re.search(r'([2]{1}[0-1]{2}[6]{1})', lrow[5]):
            _2016 += 1
        elif re.search(r'([2]{1}[0-1]{2}[7]{1})', lrow[5]):
            _2017 += 1
        elif re.search(r'([2]{1}[0-1]{2}[8]{1})', lrow[5]):
            _2018 += 1


def wrapper(filename):
    """ Perpare data for analysis """

    global FOUND
    global _2013
    global _2014
    global _2015
    global _2016
    global _2017
    global _2018

    FOUND = _2013 = _2014 = _2015 = _2016 = _2017 = _2018 = 0

    start = datetime.datetime.now()

    with open(filename) as csvfile:
        list(map(analyze, map(lambda x: x.split(','), csvfile)))

    print(f"'ao' was FOUND {FOUND} times")
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
        FOUND,
    )


if __name__ == "__main__":
    for loop in range(100):
        print(f"loop : {loop}")
        wrapper("data/dataset.csv")
