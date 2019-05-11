"""
This module uses pandas to speed up the reading and summarizing of
a million record data set
"""

from datetime import datetime
import gc
from pathlib import Path
import numpy as np
import pandas as pd

startTime = datetime.now()


def year_count(x, yr):
    """
    Returns 1 if year is in the rerocrd
    :param x:
    :param yr:
    :return: 1 or nothing
    """
    if x == yr:
        return 1


YEARS = ['2013', '2014', '2015', '2016', '2017', '2018']
FILE = pd.DataFrame(pd.read_csv(Path.cwd().with_name('data') /
                                "mega.csv", usecols=['date', 'sentence'],
                                engine='c', quotechar='"', header=0))

FILE['ao'] = np.where(FILE['sentence'].str.contains("ao", case=False,
                                                    regex=True), 1, 0)
ao_count = FILE['ao'].sum()
FILE = FILE[FILE['date'].str[-4:].isin(YEARS)]

# applies year count function to the date column
FILE['2013'] = np.vectorize(year_count)(FILE['date'].str[-2:], '13')

# sums number of records with 2013 in the date
thirteen_count = FILE['2013'].sum()

# deletes all records with 2013 in the date to reduce number of
# records and speed future searches
FILE = FILE[FILE['date'] != '2013']

FILE['2014'] = np.vectorize(year_count)(FILE['date'].str[-2:], '14')
fourteen_count = FILE['2014'].sum()
FILE = FILE[FILE['date'] != '2014']

FILE['2015'] = np.vectorize(year_count)(FILE['date'].str[-2:], '15')
fifteen_count = FILE['2015'].sum()
FILE = FILE[FILE['date'] != '2015']

FILE['2016'] = np.vectorize(year_count)(FILE['date'].str[-2:], '16')
sixteen_count = FILE['2016'].sum()
FILE = FILE[FILE['date'] != '2016']

FILE['2017'] = np.vectorize(year_count)(FILE['date'].str[-2:], '17')
seventeen_count = FILE['2017'].sum()
FILE = FILE[FILE['date'] != '2017']

FILE['2018'] = np.vectorize(year_count)(FILE['date'].str[-2:], '18')
eighteen_count = FILE['2018'].sum()
FILE = FILE[FILE['date'] != '2018']


def print_results():
    """
    Prints the record counts per year
    :return: Dictionary keys and values
    """

    results = {'2013': thirteen_count,
               '2014': fourteen_count,
               '2015': fifteen_count,
               '2016': sixteen_count,
               '2017': seventeen_count,
               '2018': eighteen_count}
    print(results)


runtime = datetime.now() - startTime


def main():
    """
    Runs the program
    """
    print_results()
    print(f'"ao" was fount {ao_count} times')
    print(f'Runtime is: {runtime}')


if __name__ == "__main__":
    main()
    gc.collect()
