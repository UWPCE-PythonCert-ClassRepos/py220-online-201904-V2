"""
poorly performing, poorly written module

"""
import csv
from datetime import datetime
from pathlib import Path
import uuid

startTime = datetime.now()

def make_large_file(infilename, filename):
    is_first, count = True, 1
    with open (infilename, 'r', newline='\n') as infile:
        with open(filename, 'w',newline='\n') as outfile:
            writer = csv.writer(outfile)
            reader = csv.reader(infile)
            header = next(reader)
            header.insert(0,'ID')
            rest = [row for row in reader]
            writer.writerow(header)
            for i in range(100000):
                for row in rest:
                    row.insert(0, uuid.uuid4())
                    writer.writerow(row)


def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                for i in range(100000):
                    new_ones.append((lrow[5], lrow[0]))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            if new[0][6:] == '2014':
                year_count["2014"] += 1
            if new[0][6:] == '2015':
                year_count["2015"] += 1
            if new[0][6:] == '2016':
                year_count["2016"] += 1
            if new[0][6:] == '2017':
                year_count["2017"] += 1
            if new[0][6:] == '2018':
                year_count["2017"] += 1

        print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')


        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1
        print(len(lrow))


        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()


        print( start, end, year_count, found)

runtime = datetime.now() - startTime


def main():
    infilename = Path.cwd().with_name('data')/"exercise.csv"
    filename = Path.cwd().with_name('data')/"mega_poor.csv"
    make_large_file(infilename, filename)
    analyze(filename)
    print(runtime)



if __name__ == "__main__":
    # import timeit
    # print(timeit.timeit("main()", number=10))
    main()
