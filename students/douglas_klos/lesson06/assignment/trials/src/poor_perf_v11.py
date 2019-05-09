#!/usr/bin/env python3

import datetime
import pandas as pd


def analyze(filename):
    found = 0

    _2013 = 0
    _2014 = 0
    _2015 = 0
    _2016 = 0
    _2017 = 0
    _2018 = 0

    start = datetime.datetime.now()

    df = pd.read_csv(filename, header=None)
    string = pd.Series(df[6])
    found = sum(string.str.contains("ao"))

    date = pd.Series(df[5])
    _2013 = sum(date.str.contains("2013"))
    _2014 = sum(date.str.contains("2014"))
    _2015 = sum(date.str.contains("2015"))
    _2016 = sum(date.str.contains("2016"))
    _2017 = sum(date.str.contains("2017"))
    _2018 = sum(date.str.contains("2018"))

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
    analyze("data/dataset.csv")


if __name__ == "__main__":
    main()
