#!/usr/bin/env python3
# pylint: disable=R0914, R0915
"""
Parallel processing with three children process.

Compatible with both Python 2 and Python 3.
"""

import datetime
from multiprocessing import Process, Queue

PROCESSES = 4
RECORDS = 1000000


def consume(start_point, consume_range, results, filename="data/dataset.csv"):
    """ Consume CSV file

    Arguments:
        start_point {int} -- Starting index into csv file
        consume_range {int} -- Range in csv file to consume
        results {multiprocessing.Queue} -- Returns values to parent process

    Keyword Arguments:
        filename {str} -- File to consume. (default: {"data/dataset.csv"})
    """
    search_results = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0,
        "found": 0,
    }

    full_list = list(open(filename))
    for loop in range(consume_range):
        lrow = full_list[loop + start_point]
        lrow = lrow.split(",")

        if "ao" in lrow[6]:
            search_results["found"] += 1

        if "2012" < lrow[5][6:] < "2019":
            if lrow[5][6:] == "2013":
                search_results["2013"] += 1
            elif lrow[5][6:] == "2014":
                search_results["2014"] += 1
            elif lrow[5][6:] == "2015":
                search_results["2015"] += 1
            elif lrow[5][6:] == "2016":
                search_results["2016"] += 1
            elif lrow[5][6:] == "2017":
                search_results["2017"] += 1
            elif lrow[5][6:] == "2018":
                search_results["2018"] += 1

    results.put(search_results)


def display_results(search_results):
    """ Displays results of consume

    Arguments:
        search_results {dict} -- Dictionary of results
    """

    # Using % notation to maintain python2 compatibility
    print("'ao' was found %d times" % search_results["found"])
    print(
        "2013:%d\t " % (search_results["2013"]) +
        "2014:%d\t " % (search_results["2014"]) +
        "2015:%d\t " % (search_results["2015"]) +
        "2016:%d\t " % (search_results["2016"]) +
        "2017:%d\t " % (search_results["2017"]) +
        "2018:%d\n" % (search_results["2018"])
    )


def analyze():
    """ Analyze setup process to create children (basically main) """

    start = datetime.datetime.now()
    filename = "data/dataset.csv"
    results = Queue()
    process_list = []
    search_results = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0,
        "found": 0,
    }

    for process_num in range(PROCESSES):
        process = Process(
            target=consume,
            args=(
                int(((RECORDS / PROCESSES) * process_num)),
                int(RECORDS / PROCESSES),
                results,
                filename,
            ),
        )
        process.start()
        process_list.append(process)

    for process in process_list:
        process.join()
        result = results.get()
        search_results["found"] += result["found"]
        search_results["2013"] += result["2013"]
        search_results["2014"] += result["2014"]
        search_results["2015"] += result["2015"]
        search_results["2016"] += result["2016"]
        search_results["2017"] += result["2017"]
        search_results["2018"] += result["2018"]

    display_results(search_results)
    end = datetime.datetime.now()

    return (start, end, search_results)


if __name__ == "__main__":
    for _ in range(10):
        analyze()
