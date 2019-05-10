#!/usr/bin/env python3
""" Parallel """

import os
import datetime
from multiprocessing import Process, Value, Array, Manager


def analyze_first_half(return_dict, filename="data/dataset.csv"):
    """ Analyze first half of file """

    counter = 0

    for lrow in open(filename):
        counter += 1
        if counter > 500000:
            return
        lrow = lrow.split(',')

        if "ao" in lrow[6]:
            return_dict['found'] += 1

        if "2012" < lrow[5][6:] < "2019":
            if lrow[5][6:] == "2013":
                return_dict["2013"] += 1
            elif lrow[5][6:] == "2014":
                return_dict["2014"] += 1
            elif lrow[5][6:] == "2015":
                return_dict["2015"] += 1
            elif lrow[5][6:] == "2016":
                return_dict["2016"] += 1
            elif lrow[5][6:] == "2017":
                return_dict["2017"]+= 1
            elif lrow[5][6:] == "2018":
                return_dict["2018"] += 1


def analyze_second_half(return_dict, filename="data/dataset2.csv"):
    """ Analyze second half of file """

    counter = 0

    for lrow in reversed(list(open(filename))):
        counter += 1
        if counter > 500000:
            return
        lrow = lrow.split(',')

        if "ao" in lrow[6]:
            return_dict['found'] += 1

        if "2012" < lrow[5][6:] < "2019":
            if lrow[5][6:] == "2013":
                return_dict["2013"] += 1
            elif lrow[5][6:] == "2014":
                return_dict["2014"] += 1
            elif lrow[5][6:] == "2015":
                return_dict["2015"] += 1
            elif lrow[5][6:] == "2016":
                return_dict["2016"] += 1
            elif lrow[5][6:] == "2017":
                return_dict["2017"]+= 1
            elif lrow[5][6:] == "2018":
                return_dict["2018"] += 1


def display_results(return_dict):
    # print("'ao' was found %d times" % return_dict.found)
    print("'ao' was found %d times\n2013:%d\t 2014:%d\t 2015: %d\t 2016:%d\t 2017:%d\t 2018:%d\n" %
          (return_dict["found"],return_dict["2013"],return_dict["2014"],return_dict["2015"],return_dict["2016"],return_dict["2017"],return_dict["2018"]))


def main():
    start = datetime.datetime.now()
    filename = "data/dataset.csv"

    manager = Manager()
    return_dict = manager.dict()

    for loop in range(10):

        return_dict['2013'] = 0
        return_dict['2014'] = 0
        return_dict['2015'] = 0
        return_dict['2016'] = 0
        return_dict['2017'] = 0
        return_dict['2018'] = 0
        return_dict['found'] = 0

        process1 = Process(target=analyze_first_half, args=(return_dict, filename))
        process2 = Process(target=analyze_second_half, args=(return_dict, filename))

        process1.start()
        process2.start()

        process1.join()
        process2.join()

        display_results(return_dict)

    end = datetime.datetime.now()

    return (
        start,
        end,
        return_dict,
    )

if __name__ == "__main__":
    main()