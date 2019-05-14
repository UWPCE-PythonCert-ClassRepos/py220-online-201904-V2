"""
good performing after modification

"""
import logging
import datetime
import csv

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def analyze_poor_perf(filename):
    '''the orginal poor_perf.py'''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in reader:
            lrow = list(row)
            if row[5] != ' date' and int(lrow[5][-4:]) >= 2012:
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
            #lrow = list(line)
            if "ao" in line[6]:
                found += 1
        print(f"'ao' was found {found} times")
    end = datetime.datetime.now()
    LOGGER.info('The original "poor_perf" takes %s', end - start)
    return (start, end, year_count, found)


def analyze_iterator(filename):
    '''using iterator to go through the records'''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        iterator = iter(reader)
        new_ones = []
        found = 0
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        while True:
            try:
                i = next(iterator)
            except StopIteration:
                break
            if read_iter_func(i):
                # builds a list with targeted years 2012+
                new_ones.append(read_iter_func(i))
                # update year_count dictionary
                year_count = count_iter_func(read_iter_func(i), year_count)
            #search for 'ao'
            found = search_iter_func(i, found)
    print(year_count)
    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()
    LOGGER.info('The "iterator" version takes %s', end - start)
    return (start, end, year_count, found)


def read_iter_func(data):
    '''a selection function that feed into iterator'''
    if data[5] != ' date' and int(data[5][-4:]) >= 2012:
        return data[5], data[0]
    return None

def count_iter_func(data, year_count_dict):
    '''a selection function that feed into iterator'''
    if data[0][6:] == '2013':
        year_count_dict["2013"] += 1
    if data[0][6:] == '2014':
        year_count_dict["2014"] += 1
    if data[0][6:] == '2015':
        year_count_dict["2015"] += 1
    if data[0][6:] == '2016':
        year_count_dict["2016"] += 1
    if data[0][6:] == '2017':
        year_count_dict["2017"] += 1
    if data[0][6:] == '2018':
        year_count_dict["2017"] += 1
    return year_count_dict

def search_iter_func(data, found):
    '''search for keyword "ao"'''
    if "ao" in data[6]:
        found += 1
    return found


def analyze_comprehension(filename):
    '''using comprehensionto go through the records'''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
        new_ones = [(row[5], row[0]) for row in reader
                    if row[5] != ' date' and int(row[5][-4:]) >= 2012]

        found_list = [1 for row in reader if "ao" in row[6]]
        found = len(found_list)

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
    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()
    LOGGER.info('The "comprehension" version takes %s', end - start)
    return (start, end, year_count, found)


def analyze_generator(filename):
    '''using generator to go through the records'''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
        new_ones = list((row[5], row[0]) for row in reader
                        if row[5] != ' date' and int(row[5][-4:]) >= 2012)
        found_list = list(1 for row in reader if "ao" in row[6])
        found = len(found_list)
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
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()
        LOGGER.info('The "generator" version takes %s', end - start)
    return (start, end, year_count, found)


def analyze_map(filename):
    '''using map to go through the records'''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
        new_ones_ll = filter(filter_func, reader)
        new_ones = map(map_func, new_ones_ll)

        found_list = filter(filter_search_func, reader)
        found = len(list(found_list))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        for new in list(new_ones):
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
    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()
    LOGGER.info('The "filter" version takes %s', end - start)
    return (start, end, year_count, found)

def filter_func(row):
    '''filter with years greater than and equal to 2012'''
    if row[5] != ' date' and int(row[5][-4:]) >= 2012:
        return row
    return None

def map_func(row):
    '''map with row index 5 and 0'''
    return row[5], row[0]

def filter_search_func(row):
    '''search for "ao" in input'''
    if "ao" in row[6]:
        return row
    return None

def analyze(filename):
    '''the main function calls'''
    analyze_poor_perf(filename)
    analyze_iterator(filename)
    analyze_comprehension(filename)
    analyze_generator(filename)
    analyze_map(filename)

if __name__ == "__main__":
    #FILENAME = "../data/exercise.csv"
    FILENAME = "../data/exercise2.csv"
    analyze(FILENAME)
