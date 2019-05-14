#!/usr/bin/env python3
#pylint: disable=R0914, R0915
""" Parallel processing with three children processes. """

import datetime
from multiprocessing import Process, Value

RECORDS = 1000000
FIRST = 400000
SECOND = 300000
THIRD = 300000


def consume_1(found, _2013, _2014, _2015, _2016,
              _2017, _2018, filename="data/dataset.csv"):
    """ Consume first part of file """

    counter = 0

    for lrow in open(filename):
        counter += 1
        if counter > FIRST:
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


def consume_2(found, _2013, _2014, _2015, _2016,
              _2017, _2018, consume_range, start_point,
              filename="data/dataset.csv",):
    """ Consume repeating part of file """

    counter = 0
    full_list = list(open(filename))
    for loop in range(consume_range):
        lrow = full_list[loop + start_point]
        counter += 1
        if counter > SECOND:
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


def display_results(found, _2013, _2014, _2015, _2016, _2017, _2018):
    """ Display results """
    print(f"'ao' was found {found} times")
    print(
        f"2013:{_2013}\t"
        f"2014:{_2014}\t"
        f"2015:{_2015}\t"
        f"2016:{_2016}\t"
        f"2017:{_2017}\t"
        f"2018:{_2018}\n"
    )


def main():
    """ main for three process parallel version """
    start = datetime.datetime.now()
    filename = "data/dataset.csv"

    found_1 = Value("i", 0)
    _2013_1 = Value("i", 0)
    _2014_1 = Value("i", 0)
    _2015_1 = Value("i", 0)
    _2016_1 = Value("i", 0)
    _2017_1 = Value("i", 0)
    _2018_1 = Value("i", 0)

    found_2 = Value("i", 0)
    _2013_2 = Value("i", 0)
    _2014_2 = Value("i", 0)
    _2015_2 = Value("i", 0)
    _2016_2 = Value("i", 0)
    _2017_2 = Value("i", 0)
    _2018_2 = Value("i", 0)

    found_3 = Value("i", 0)
    _2013_3 = Value("i", 0)
    _2014_3 = Value("i", 0)
    _2015_3 = Value("i", 0)
    _2016_3 = Value("i", 0)
    _2017_3 = Value("i", 0)
    _2018_3 = Value("i", 0)

    for _ in range(10):

        found_1.value = 0
        _2013_1.value = 0
        _2014_1.value = 0
        _2015_1.value = 0
        _2016_1.value = 0
        _2017_1.value = 0
        _2018_1.value = 0

        found_2.value = 0
        _2013_2.value = 0
        _2014_2.value = 0
        _2015_2.value = 0
        _2016_2.value = 0
        _2017_2.value = 0
        _2018_2.value = 0

        found_3.value = 0
        _2013_3.value = 0
        _2014_3.value = 0
        _2015_3.value = 0
        _2016_3.value = 0
        _2017_3.value = 0
        _2018_3.value = 0

        process1 = Process(
            target=consume_1,
            args=(
                found_1,
                _2013_1,
                _2014_1,
                _2015_1,
                _2016_1,
                _2017_1,
                _2018_1,
                filename,
            ),
        )
        process2 = Process(
            target=consume_2,
            args=(
                found_2,
                _2013_2,
                _2014_2,
                _2015_2,
                _2016_2,
                _2017_2,
                _2018_2,
                SECOND,
                FIRST,
                filename,
            ),
        )
        process3 = Process(
            target=consume_2,
            args=(
                found_3,
                _2013_3,
                _2014_3,
                _2015_3,
                _2016_3,
                _2017_3,
                _2018_3,
                THIRD,
                FIRST + SECOND,
                filename,
            ),
        )

        process1.start()
        process2.start()
        process3.start()

        process1.join()
        process2.join()
        process3.join()

        found_total = found_1.value + found_2.value + found_3.value
        _2013_total = _2013_1.value + _2013_2.value + _2013_3.value
        _2014_total = _2014_1.value + _2014_2.value + _2014_3.value
        _2015_total = _2015_1.value + _2015_2.value + _2015_3.value
        _2016_total = _2016_1.value + _2016_2.value + _2016_3.value
        _2017_total = _2017_1.value + _2017_2.value + _2017_3.value
        _2018_total = _2018_1.value + _2018_2.value + _2018_3.value

        display_results(
            found_total,
            _2013_total,
            _2014_total,
            _2015_total,
            _2016_total,
            _2017_total,
            _2018_total,
        )

    end = datetime.datetime.now()

    return (
        start,
        end,
        {
            "2013": _2013_total,
            "2014": _2014_total,
            "2015": _2015_total,
            "2016": _2016_total,
            "2017": _2017_total,
            "2018": _2018_total,
        },
        found_total,
    )


if __name__ == "__main__":
    main()
