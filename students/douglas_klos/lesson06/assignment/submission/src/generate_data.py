#!/usr/bin/env python3
#pylint: disable=W0611

""" Generates random data for testing """

import time
import uuid
from random import randint, random
from essential_generators import (
    DocumentGenerator,
    StatisticTextGenerator,
    MarkovTextGenerator,
    MarkovWordGenerator
)

RECORDS = 1000000


def generate_rows():
    """ Generate a row of random data """
    range_start = 10 ** (16 - 1)
    range_end = (10 ** 16) - 1

    # gen = DocumentGenerator(
    #     text_generator=MarkovTextGenerator(),
    #     word_generator=MarkovWordGenerator(),
    # )
    gen = DocumentGenerator(
        text_generator=StatisticTextGenerator(),
        word_generator=StatisticTextGenerator(),
    )

    for record in range(RECORDS):

        yield f"{record},"\
              f"{uuid.uuid4()},"\
              f"{record},"\
              f"{record},"\
              f"{randint(range_start, range_end)},"\
              f"{rand_date('1/1/1900', '1/1/2020', '%m/%d/%Y', random())},"\
              f"{gen.sentence().replace(',', '')}"\
              f"\n"


def rand_date(start, end, _format, seed):
    """ Generates a random date between start and end """
    start_time = time.mktime(time.strptime(start, _format))
    end_time = time.mktime(time.strptime(end, _format))
    rand_time = start_time + seed * (end_time - start_time)
    return time.strftime(_format, time.localtime(rand_time))


def write_csv_file():
    """ Writes our new CSV file """
    with open("./data/dataset.csv", "w", newline="\n") as csv_file:
        csv_file.writelines(generate_rows())


if __name__ == "__main__":
    write_csv_file()


# 1,000,000 records.
# real	0m44.312s
# user	0m41.700s
# sys	0m2.612s
