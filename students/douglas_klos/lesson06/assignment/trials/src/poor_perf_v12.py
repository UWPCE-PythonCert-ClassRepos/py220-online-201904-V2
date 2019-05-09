#!/usr/bin/env python3

import datetime
import pandas as pd


def analyze(filename):
    start = datetime.datetime.now()
    df = pd.read_csv(filename, header=None)
    string = pd.Series(df[6])
    date = pd.Series(df[5])
    return (
        start,
        datetime.datetime.now(),
        {
            "2013": sum(date.str.contains("2013")),
            "2014": sum(date.str.contains("2014")),
            "2015": sum(date.str.contains("2015")),
            "2016": sum(date.str.contains("2016")),
            "2017": sum(date.str.contains("2017")),
            "2018": sum(date.str.contains("2018")),
        },
        sum(string.str.contains("ao")),
    )


def main():
    analyze("data/dataset.csv")


if __name__ == "__main__":
    main()
