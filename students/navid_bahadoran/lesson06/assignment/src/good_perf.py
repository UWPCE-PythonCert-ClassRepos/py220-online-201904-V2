# pylint: disable =
""" This program is to check the performance of CSV reader and writer"""
import pathlib
import os
import datetime
import csv

ASSIGNMENT_FOLDER = pathlib.Path(__file__).parents[1]
CSV_FILE = ASSIGNMENT_FOLDER / "data/exercise.csv"


def analyze(filename):
    """ analyze the csv file that I made"""
    start = datetime.datetime.now()
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    found = 0
    with open(filename, "r", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if row[5][6:] == '2013':
                year_count["2013"] += 1
            elif row[5][6:] == '2014':
                year_count["2014"] += 1
            elif row[5][6:] == '2015':
                year_count["2015"] += 1
            elif row[5][6:] == '2016':
                year_count["2016"] += 1
            elif row[5][6:] == '2017':
                year_count["2017"] += 1
            elif row[5][6:] == '2018':
                year_count["2018"] += 1
            if "ao" in row[6]:
                found += 1

    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()
    print(year_count)
    return (start, end, year_count, found)


def main():
    """ main function to run the program"""
    filename = CSV_FILE
    analyze(filename)


if __name__ == "__main__":
    main()
