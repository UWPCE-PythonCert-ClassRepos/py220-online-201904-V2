#!/usr/bin/env python2.7
#pylint: disable=R0914, R0915
"""
Parallel processing with three children process.

I've written this to work with both Python 2 and Python 3.
If I were writing it for just Python 3 I'd use f-strings instead
of % notation.  However, since this was performance week, Python 2
executes the code more quickly, so it's been written to be legacy
compliant.
"""

import datetime
from multiprocessing import Process, Value

# We're defining the total number of records to consume
#   and the number of records per process to consume.
RECORDS = 1000000
FIRST = 400000
SECOND = 300000
THIRD = 300000


def consume_1(found, _2013, _2014, _2015, _2016, _2017, _2018,
              consume_range, filename="data/dataset.csv"):
    """
    Consume first part of file

    The first part of the file we can consume with an iterator,
    however as we don't want to process the entire file, we need to
    break out after our counter has incremented enough.
    """

    counter = 0
    for lrow in open(filename):
        counter += 1
        if counter > consume_range:
            return
        lrow = lrow.split(",")

        if "ao" in lrow[6]:
            found.value += 1

        # The additional '< "2019"' on the end of this if is highly dependent
        #   on the number of dates in the dataset with beyond 2018.  If
        #   there are very few this will result in more overhead.  If there
        #   are many, it will result in saved colock cycles.
        if "2012" < lrow[5][6:] < "2019":
            if lrow[5][6:] == "2013":
                _2013.value += 1
            elif lrow[5][6:] == "2014":
                _2014.value += 1
            elif lrow[5][6:] == "2015":
                _2015.value += 1
            elif lrow[5][6:] == "2016":
                _2016.value += 1
            elif lrow[5][6:] == "2017":
                _2017.value += 1
            elif lrow[5][6:] == "2018":
                _2018.value += 1


def consume_2(found, _2013, _2014, _2015, _2016, _2017, _2018,
              consume_range, start_point, filename="data/dataset.csv",):
    """
    Consume repeating part of file

    Consume_2 we must first read the entire file into a list so that we can
    start in the file at our specified location.  We don't need to keep
    track of a counter here, we loop through consume_range
    """

    full_list = list(open(filename))
    for loop in range(consume_range):
        lrow = full_list[loop + start_point]
        lrow = lrow.split(",")

        if "ao" in lrow[6]:
            found.value += 1

        if "2012" < lrow[5][6:] < "2019":
            if lrow[5][6:] == "2013":
                _2013.value += 1
            elif lrow[5][6:] == "2014":
                _2014.value += 1
            elif lrow[5][6:] == "2015":
                _2015.value += 1
            elif lrow[5][6:] == "2016":
                _2016.value += 1
            elif lrow[5][6:] == "2017":
                _2017.value += 1
            elif lrow[5][6:] == "2018":
                _2018.value += 1


def display_results(found, _2013, _2014, _2015, _2016, _2017, _2018):
    """ Display results """

    # If this were strictly for Python 3 I'd use f-string.
    #   But 2 run this faster, and it's performance week.
    #   And in lieu of supporting two files every time I do a tweak
    #   I'm just making the thing legacy python compatible.
    print("'ao' was found %d times" % found)
    print(
        "2013:%d\t " % (_2013) +
        "2014:%d\t " % (_2014) +
        "2015:%d\t " % (_2015) +
        "2016:%d\t " % (_2016) +
        "2017:%d\t " % (_2017) +
        "2018:%d\n" % (_2018)
    )


def analyze():
    """ Analyze setup process to create children """
    start = datetime.datetime.now()
    filename = "data/dataset.csv"

    # UFF!!! ALL THESE DECLARATIONS!!!
    #   So integers are faster than dictionaries, that hash lookup
    #   takes clock cycles.  Next, we need to declare a set of counter
    #   variables for each child process we're about to spawn.  We need
    #   return values from the proccess, so we need to allocate memory for
    #   them.  That's what we're doing here.  I could have written a loop
    #   to do this in less lines of code, but it results in more clock
    #   cycles to complete the task.

    # I tried this with global variabels before this, will all process
    #   trying to operate on them, and while it appeared to work, once
    #   the process was lost so were the results.  I also tried passing
    #   a single set of shared memory variabes to all consume functions
    #   this gave very strange results, the result would come up just a bit
    #   different every run.  I'd be expecting 8362, and I'd get 8320-8362.

    found_1 = Value("i", 0)
    _2013_1 = Value("i", 0)
    _2014_1 = Value("i", 0)
    _2015_1 = Value("i", 0)
    _2016_1 = Value("i", 0)
    _2017_1 = Value("i", 0)
    _2018_1 = Value("i", 0)

    found_2 = Value("i", 0)
    _2013_2 = Value("i", 0)
    _2014_2 = Value("i", 0)
    _2015_2 = Value("i", 0)
    _2016_2 = Value("i", 0)
    _2017_2 = Value("i", 0)
    _2018_2 = Value("i", 0)

    found_3 = Value("i", 0)
    _2013_3 = Value("i", 0)
    _2014_3 = Value("i", 0)
    _2015_3 = Value("i", 0)
    _2016_3 = Value("i", 0)
    _2017_3 = Value("i", 0)
    _2018_3 = Value("i", 0)

    # Loop was used to run the program multiple times for better results on
    #   a higher-performing system.  A single test of say .5 sec was less
    #   reliable than 10 tests at 4.95 seconds.  Reset to 1 loop for submission
    #   in case grading is done on a potato.
    for _ in range(1):

        # Need to make sure our pile of variables are 0'd out.
        found_1.value = 0
        _2013_1.value = 0
        _2014_1.value = 0
        _2015_1.value = 0
        _2016_1.value = 0
        _2017_1.value = 0
        _2018_1.value = 0

        found_2.value = 0
        _2013_2.value = 0
        _2014_2.value = 0
        _2015_2.value = 0
        _2016_2.value = 0
        _2017_2.value = 0
        _2018_2.value = 0

        found_3.value = 0
        _2013_3.value = 0
        _2014_3.value = 0
        _2015_3.value = 0
        _2016_3.value = 0
        _2017_3.value = 0
        _2018_3.value = 0

        # Here we define and spawn each process.
        process1 = Process(
            target=consume_1,
            args=(
                found_1,
                _2013_1,
                _2014_1,
                _2015_1,
                _2016_1,
                _2017_1,
                _2018_1,
                FIRST,
                filename,
            ),
        )
        process1.start()

        process2 = Process(
            target=consume_2,
            args=(
                found_2,
                _2013_2,
                _2014_2,
                _2015_2,
                _2016_2,
                _2017_2,
                _2018_2,
                SECOND,
                FIRST,
                filename,
            ),
        )
        process2.start()

        process3 = Process(
            target=consume_2,
            args=(
                found_3,
                _2013_3,
                _2014_3,
                _2015_3,
                _2016_3,
                _2017_3,
                _2018_3,
                THIRD,
                FIRST + SECOND,
                filename,
            ),
        )
        process3.start()

        # Wait for the processes to finish
        process1.join()
        process2.join()
        process3.join()

        # Add up the values of all that shared ram
        found_total = found_1.value + found_2.value + found_3.value
        _2013_total = _2013_1.value + _2013_2.value + _2013_3.value
        _2014_total = _2014_1.value + _2014_2.value + _2014_3.value
        _2015_total = _2015_1.value + _2015_2.value + _2015_3.value
        _2016_total = _2016_1.value + _2016_2.value + _2016_3.value
        _2017_total = _2017_1.value + _2017_2.value + _2017_3.value
        _2018_total = _2018_1.value + _2018_2.value + _2018_3.value

        # And we get results
        display_results(
            found_total,
            _2013_total,
            _2014_total,
            _2015_total,
            _2016_total,
            _2017_total,
            _2018_total,
        )

    end = datetime.datetime.now()

    return (
        start,
        end,
        {
            "2013": _2013_total,
            "2014": _2014_total,
            "2015": _2015_total,
            "2016": _2016_total,
            "2017": _2017_total,
            "2018": _2018_total,
        },
        found_total,
    )


if __name__ == "__main__":
    analyze()
