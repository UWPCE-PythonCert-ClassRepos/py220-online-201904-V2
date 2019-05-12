#!/usr/bin/env python3
""" Better performing module #14 """

import datetime


def analyze(filename):
    """ Analyze input filename for some arbitray, but consistent, data """

    counter = -1
    found = 0
    _2013 = 0
    _2014 = 0
    _2015 = 0
    _2016 = 0
    _2017 = 0
    _2018 = 0

    start = datetime.datetime.now()

    with open(filename, 'rb') as csvfile:
        # for line in csvfile:
        contents = csvfile.read().decode("utf-8")
        # for line in contents:
        # print(contents)
        lrow = contents.split(',')
        for row in lrow:
            counter += 1
            # print(f"coutner = {counter}")
            print(f"row data {row}")
            if (counter == 5):
                if 'ao' in lrow:
                    found += 1
                counter = -1

            if (counter == 4):
                last_four = int(row[-4:])
                # print(last_four)
                if (last_four > 2012):
                    if (last_four == 2013):
                        _2013 += 1
                    if (last_four == 2014):
                        _2014 += 1
                    if (last_four == 2015):
                        _2015 += 1
                    if (last_four == 2016):
                        _2016 += 1
                    if (last_four == 2017):
                        _2017 += 1
                    if (last_four == 2018):
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


if __name__ == "__main__":
    analyze("data/dataset.csv")
