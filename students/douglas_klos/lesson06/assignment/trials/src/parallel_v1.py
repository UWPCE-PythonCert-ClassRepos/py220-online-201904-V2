#!/usr/bin/env python3
""" Parallel """

import os
import datetime
from multiprocessing import Process, Value, Array


def analyze_first_half(found, _2013, _2014, _2015, _2016, _2017, _2018, filename="data/dataset.csv"):
    """ Analyze first half of file """

    first_half_counter = 0

    

    for lrow in list(open(filename)):
        # for lrow in csvfile:
        first_half_counter += 1
        if first_half_counter > 499999:
            return
        lrow = lrow.split(',')
        # print(lrow)

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

    second_half_counter = 0

    # with open(filename) as csvfile:
    for lrow in reversed(list(open(filename))):
    # for lrow in reversed(csvfile):
        second_half_counter += 1
        if second_half_counter > 499999:
            return
        lrow = lrow.split(',')
        # print(lrow)

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

    print(f"'ao' was found {found.value} times")
    print(
        f"2013:{_2013.value}\t"
        f"2014:{_2014.value}\t"
        f"2015:{_2015.value}\t"
        f"2016:{_2016.value}\t"
        f"2017:{_2017.value}\t"
        f"2018:{_2018.value}\n"
    )


if __name__ == "__main__":

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

    # return (
    #     # start,
    #     # end,
    #     {
    #         "2013": _2013,
    #         "2014": _2014,
    #         "2015": _2015,
    #         "2016": _2016,
    #         "2017": _2017,
    #         "2018": _2018,
    #     },
    #     found,
    # )




# total_found = 0
# total_2013 = 0
# total_2014 = 0
# total_2015 = 0
# total_2016 = 0
# total_2017 = 0
# total_2018 = 0