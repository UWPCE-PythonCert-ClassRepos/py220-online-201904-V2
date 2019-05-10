#!/usr/bin/env python3
""" Parallel """

import os
import datetime
from multiprocessing import Process, Value, Array


def analyze_first_half(found, _2013, _2014, _2015, _2016, _2017, _2018, filename="data/dataset.csv"):
    """ Analyze first half of file """

    counter = 0

    for lrow in open(filename):
        counter += 1
        if counter > 525000:
            return
        lrow = lrow.split(',')

        if "ao" in lrow[6]:
            found.value += 1

        if "2012" < lrow[5][6:] < "2019":
            if lrow[5][6:] == "2013":
                _2013.value += 1
            elif lrow[5][6:] == "2014":
                _2014.value += 1
            elif lrow[5][6:] == "2015":
                _2015.value += 1
            elif lrow[5][6:] == "2016":
                _2016.value += 1
            elif lrow[5][6:] == "2017":
                _2017.value += 1
            elif lrow[5][6:] == "2018":
                _2018.value += 1


def analyze_second_half(found, _2013, _2014, _2015, _2016, _2017, _2018, filename="data/dataset.csv"):
    """ Analyze second half of file """

    counter = 0

    for lrow in reversed(list(open(filename))):
        counter += 1
        if counter > 475000:
            return
        lrow = lrow.split(',')

        if "ao" in lrow[6]:
            found.value += 1

        if "2012" < lrow[5][6:] < "2019":
            if lrow[5][6:] == "2013":
                _2013.value += 1
            elif lrow[5][6:] == "2014":
                _2014.value += 1
            elif lrow[5][6:] == "2015":
                _2015.value += 1
            elif lrow[5][6:] == "2016":
                _2016.value += 1
            elif lrow[5][6:] == "2017":
                _2017.value += 1
            elif lrow[5][6:] == "2018":
                _2018.value += 1


def display_results(found, _2013, _2014, _2015, _2016, _2017, _2018):

    print("'ao' was found %d times" % found.value)
    print("2013:%d\t 2014:%d\t 2015: %d\t 2016:%d\t 2017:%d\t 2018:%d\n" %
          (_2013.value, _2014.value, _2015.value, _2016.value, _2017.value, _2018.value))




def main():
    start = datetime.datetime.now()
    filename = "data/dataset.csv"

    found = Value('i', 0)
    _2013 = Value('i', 0)
    _2014 = Value('i', 0)
    _2015 = Value('i', 0)
    _2016 = Value('i', 0)
    _2017 = Value('i', 0)
    _2018 = Value('i', 0)

    for loop in range(10):

        found.value = 0
        _2013.value = 0
        _2014.value = 0
        _2015.value = 0
        _2016.value = 0
        _2017.value = 0
        _2018.value = 0

        process1 = Process(target=analyze_first_half, args=(found, _2013, _2014, _2015, _2016, _2017, _2018, filename))
        process2 = Process(target=analyze_second_half, args=(found, _2013, _2014, _2015, _2016, _2017, _2018, filename))
        process1.start()
        process2.start()
        
        process1.join()
        process2.join()

        display_results(found, _2013, _2014, _2015, _2016, _2017, _2018)

    end = datetime.datetime.now()

    return (
        start,
        end,
        {
            "2013": _2013.value,
            "2014": _2014.value,
            "2015": _2015.value,
            "2016": _2016.value,
            "2017": _2017.value,
            "2018": _2018.value,
        },
        found,
    )

if __name__ == "__main__":
    main()