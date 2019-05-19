import datetime
import lorem
import faker
import random
import string
import csv
import uuid


def analyze(filename):
    """loops through each year looking for ao using condition statments"""
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
    """generates random fake data to populate 1000000 records"""
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
    for i in range(num_records - 10 + 1):
        seq = 10 + i
        guid = str(uuid.uuid4())
        ccnumber = ''.join(random.choice(string.digits) for _ in range(16))
        date = fake.date_between(start_date='-75y', end_date='+50y').strftime('%m/%d/%Y')
        sentence = lorem.sentence()
        new_record = '%s,%s,%s,%s,%s,%s,%s\n' % (seq, guid, seq, seq, ccnumber, date, sentence)
        # print(new_record)
        new_records.append(new_record)

    with open(outfile, 'a') as ofile:
        ofile.writelines(new_records)


def main():
    """puts random generated data in the random.csv file"""

    data_file_name = "../data/random.csv"

    filename = "../data/exercise.csv"
    generate_random_data(filename, data_file_name)

    analyze(data_file_name)


if __name__ == "__main__":
    main()
