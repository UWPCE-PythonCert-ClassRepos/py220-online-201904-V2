"""
poorly performing, poorly written module

"""
import csv
from datetime import datetime
from functools import wraps
from pathlib import Path
import time

start = datetime.now()

filename = Path.cwd().with_name('data') / "mega.csv"
data_set = []


def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        end = time.perf_counter()
        run_time = end - start
        print(f'Process {f.__name__!r} runs in {run_time} seconds.')
        return result

    return wrapper


@timer
def analyze(filename):
    with open(filename, 'r', newline='\n') as infile:
        reader = csv.reader(infile)
        for row in reader:
            data_set.append(row)
    new_ones = []
    for i in data_set:
        if i[3][-4:] != 'date':
            new_ones.append(int(i[3][-4:]))

    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    for new in new_ones:
        if new == 2013:
            year_count["2013"] += 1
        if new == 2014:
            year_count["2014"] += 1
        if new == 2015:
            year_count["2015"] += 1
        if new == 2016:
            year_count["2016"] += 1
        if new == 2017:
            year_count["2017"] += 1
        if new == 2018:
            year_count["2017"] += 1

    print(year_count)

    found = 0
    with open(filename, 'r', newline='\n') as infile:
        reader = csv.reader(infile)
        for line in reader:
            lrow = list(line)
            if "ao" in line[4]:
                found += 1
        print(len(lrow))

    print(f"'ao' was found {found} times")
    end = datetime.now()
    print(start, end, year_count, found)


def main():
    analyze(filename)

if __name__ == "__main__":
    main()

