# pylint: disable=W0612, C0103, C0301, W0622
'''
So, this is my attempt to create the csv file.  I really think it's clunky, but
I'm also not very good at comprehensions yet.
'''

import sys
import csv
import uuid
import random
import string
import time


def daterange(start, end, format, prop):
    '''
    Setting date information
    '''
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    '''
    Randomizing the dates
    '''
    return daterange(start, end, '%m/%d/%Y', prop)


def random_string(n):
    '''
    Creates a random string of (n) characters long.
    '''
    count = 0
    s = ''
    while count < n:
        s += random.choice(string.ascii_lowercase + ' ')
        count += 1
    return s


def exercise_writer(filename, seq):
    '''
    This /should/ write the csv file
    '''
    date = randomDate('1/1/1910', '1/1/2031', random.random())
    number = random.randrange(345621524909394, 70000000000000000)
    row = (seq, uuid.uuid4(), seq, seq, number, date, random_string(64) + '.')
    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(row)


def run_csv_writer(filename):
    '''
    experiment... So, now I know what I was doing wrong.  I'd refactor this,
    but I want to actually get started on the assignment.  If I have time before
    the end I'll get it all down some.
    '''
    seq = 10
    while seq <= 1000000:
        exercise_writer(filename, seq)
        seq += 1


def main():
    '''
    Main run list
    '''
    try:
        filename = sys.argv[1]
    except IndexError:
        print('You must pass in a filename')
        sys.exit(1)
    run_csv_writer(filename)


if __name__ == '__main__':
    main()
