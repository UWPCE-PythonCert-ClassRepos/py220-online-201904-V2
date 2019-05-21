import datetime
import lorem
import faker
import random
import string
import csv
import uuid
import timeit

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
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
                year_count["2018"] += 1

        print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


def analyze_v2(filename):

    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    found = 0

    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:

            lrow = list(row)

            year = lrow[5][6:]

            if '2013' <= year <= '2018':
                if year == '2013':
                    year_count["2013"] += 1
                elif year == '2014':
                    year_count["2014"] += 1
                elif year == '2015':
                    year_count["2015"] += 1
                elif year == '2016':
                    year_count["2016"] += 1
                elif year == '2017':
                    year_count["2017"] += 1
                else:
                    year_count["2018"] += 1

            if "ao" in lrow[6]:
                found += 1

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return start, end, year_count, found


def generate_random_data(infile, outfile):
    original_data = []
    with open(infile, 'r') as ifile:
        # original_data = [line.rstrip('\n') for line in ifile.readlines()]
        original_data = ifile.readlines()
    # print(original_data)

    with open(outfile, 'w') as ofile:
        for line in original_data:
            ofile.write(line)

    fake = faker.Faker()

    num_records = 1000000
    new_records = list()
    for i in range(num_records-10+1):
        seq = 10+i
        guid = str(uuid.uuid4())
        ccnumber = ''.join(random.choice(string.digits) for _ in range(16))
        date = fake.date_between(start_date='-75y', end_date='+50y').strftime('%m/%d/%Y')
        sentence = lorem.sentence()
        new_record = '%s,%s,%s,%s,%s,%s,%s\n' % (seq, guid, seq, seq, ccnumber, date, sentence)
        # print(new_record)
        new_records.append(new_record)

    with open(outfile, 'a') as ofile:
        ofile.writelines(new_records)


def perf_analyze():
    # analyze("../data/exercise.csv")
    analyze("../data/random.csv")

def perf_analyze_v2():
    # analyze("../data/exercise.csv")
    analyze_v2("../data/random.csv")


def main():

    filename = "../data/exercise.csv"
    data_file_name = "../data/random.csv"
    # generate_random_data(filename, data_file_name)

    # analyze(data_file_name)

    # analyze(filename)

    # baseline timing from original
    timing = timeit.timeit("perf_analyze()", setup="from __main__ import perf_analyze", number=3)
    print('Runtime (secs) of original function (analyze): %s' % timing)

    # timing our modification
    timing = timeit.timeit("perf_analyze_v2()", setup="from __main__ import perf_analyze_v2", number=3)
    print('Runtime (secs) of improved function(analyze_v2): %s' % timing)

if __name__ == "__main__":
    main()
