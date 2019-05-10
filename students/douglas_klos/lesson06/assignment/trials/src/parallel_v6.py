#!/usr/bin/env python3
""" Parallel """

import os
import datetime
from multiprocessing import Process, Value, Array


def consume_forward(found, _2013, _2014, _2015, _2016, _2017, _2018, dataset):
    """ Analyze first half of file """

    first_half_counter = 0

    for lrow in dataset:
        first_half_counter += 1
        if first_half_counter > 500000:
            return
        lrow = lrow.split(",")

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


def consume_backward(found, _2013, _2014, _2015, _2016, _2017, _2018, dataset):
    """ Analyze first half of file """

    first_half_counter = 0

    for lrow in dataset:
        first_half_counter += 1
        if first_half_counter > 500000:
            return
        lrow = lrow.split(",")

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


def generate_csv():
    for value in open('./data/dataset.csv'):
        yield value
    # yield list(open('./data/dataset.csv')).readline()


def generate_reverse_csv():
    for value in reversed(list(open('./data/dataset.csv'))):
        yield value


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


def main():
    start = datetime.datetime.now()
    filename = "data/dataset.csv"

    found = Value("i", 0)
    _2013 = Value("i", 0)
    _2014 = Value("i", 0)
    _2015 = Value("i", 0)
    _2016 = Value("i", 0)
    _2017 = Value("i", 0)
    _2018 = Value("i", 0)

    for loop in range(1):
        csvfile = list(open(filename))

        found.value = 0
        _2013.value = 0
        _2014.value = 0
        _2015.value = 0
        _2016.value = 0
        _2017.value = 0
        _2018.value = 0

        process1 = Process(
            target=consume_forward,
            args=(found, _2013, _2014, _2015, _2016, _2017, _2018, generate_csv()),
        )
        process1.start()
        process2 = Process(
            target=consume_backward,
            args=(found, _2013, _2014, _2015, _2016, _2017, _2018, generate_reverse_csv()),
        )
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
