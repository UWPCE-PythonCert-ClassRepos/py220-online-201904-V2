from datetime import datetime
import functools
import gc
import numpy as np
import pandas as pd
from pathlib import Path

pd.set_option('display.max.columns', 25)
desired_width = 400
pd.set_option('display.width', desired_width)

startTime = datetime.now()


def year_count(x, yr):
    if x == yr:
        return 1
    else:
        return 0


years = ['2013', '2014', '2015', '2016', '2017', '2018']
file = pd.DataFrame(pd.read_csv(Path.cwd().with_name('data') /
                                "exercise.csv", usecols=[0, 4, 5, 6],
                                engine='c', quotechar='"', header=0)) \
    .rename(columns={'guid                                ': 'guid',
                     'date      ': 'date'})
for i in range(17):
    new = file.copy(deep=True)
    file = file.append(new, ignore_index=True)
file = file[:1000000]
# file['guid'] = range(len(file))
file['guid'] = file.index
file['ao'] = np.where(file['sentence'].str.contains("ao", case=False,
                                                    regex=True), 1, 0)
ao_count = file['ao'].sum()
file = file[file['date'].str[-4:].isin(years)]

file['2013'] = np.vectorize(year_count)(file['date'].str[-4:], '2013')
file['2014'] = np.vectorize(year_count)(file['date'].str[-4:], '2014')
file['2015'] = np.vectorize(year_count)(file['date'].str[-4:], '2015')
file['2016'] = np.vectorize(year_count)(file['date'].str[-4:], '2016')
file['2017'] = np.vectorize(year_count)(file['date'].str[-4:], '2017')
file['2018'] = np.vectorize(year_count)(file['date'].str[-4:], '2018')
thirt_count = file['2013'].sum()
fourt_count = file['2014'].sum()
fift_count = file['2015'].sum()
sixt_count = file['2016'].sum()
sevent_count = file['2017'].sum()
eight_count = file['2018'].sum()


def print_results():
    results = {'2013': thirt_count,
               '2014': fourt_count,
               '2015': fift_count,
               '2016': sixt_count,
               '2017': sevent_count,
               '2018': eight_count}
    print(results)


mega = file.to_csv(Path.cwd().with_name('data') / "mega.csv")

runtime = datetime.now() - startTime


def main():
    print_results()
    print(f'"ao" was fount {ao_count} times')
    print(f'Runtime is: {runtime}')


if __name__ == "__main__":
    main()
    gc.collect()
