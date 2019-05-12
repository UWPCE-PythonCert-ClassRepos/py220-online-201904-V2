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

YEARS = ['2013', '2014', '2015', '2016', '2017', '2018']

# read in file
FILE = pd.DataFrame(pd.read_csv(Path.cwd().with_name('data') /
                                "mega.csv", usecols=['date', 'sentence'],
                                engine='c', quotechar='"', header=0))

# column mark sentences containing 'ao' with a 1
FILE['ao'] = np.where(FILE['sentence'].str.contains("ao", case=False,
                                                    regex=True), 1, 0)

# sum of 'ao' columns
ao_count = FILE['ao'].sum()

# FILE = FILE[FILE['date'].str[-4:].isin(YEARS)]

# get year only from data
FILE['year'] = FILE['date'].str[-4:]

# create dictionary of year counts
year_count_one = dict(FILE.groupby(['year'])['year'].count())

# filter dictionary for only years 2013 - 2018
year_count_two = {k: v
                  for k, v in year_count_one.items()
                  if k in YEARS}

# add missing years to dictionary with value of 0
for i in YEARS:
    if i not in year_count_two.keys():
        year_count_two[i] = 0

runtime = datetime.now() - startTime


def main():
    """
    Runs the program
    """
    print(year_count_two)
    print(f'"ao" was fount {ao_count} times')
    print(f'Runtime is: {runtime}')


if __name__ == "__main__":
    main()
    gc.collect()
