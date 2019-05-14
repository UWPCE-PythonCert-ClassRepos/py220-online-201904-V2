#!/usr/bin/env python3
""" Module #14  - The Chosen Single Thread Python Implementation"""

import datetime


def analyze(filename):
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
            lrow = line.split(",")

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
    # Loop was used to run the program multiple times for better results on
    #   a higher-performing system.  A single test of say .5 sec was less
    #   reliable than 10 tests at 4.95 seconds.  Reset to 1 loop for submission
    #   in case grading is done on a potato.
    for loop in range(1):
        print(f"loop : {loop}")
        analyze("data/dataset.csv")
