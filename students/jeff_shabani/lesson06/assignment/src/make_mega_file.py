"""
This module takes original exercise file and creates a
new file with 1,000,000 records.
"""

from datetime import datetime
import gc
import numpy as np
from pathlib import Path
import pandas as pd

startTime = datetime.now()

pd.options.display.float_format = '{:0,.2f}'.format
pd.set_option('display.max.columns', 25)
desired_width = 400
pd.set_option('display.width', desired_width)

read = pd.read_excel

file = pd.DataFrame(pd.read_csv(Path.cwd().with_name('data') / "exercise.csv",
                                usecols=[0, 4, 5, 6], engine='c', quotechar='"',
                                header=0)) \
    .rename(columns={'guid': 'guid', 'date      ': 'date'})

# change certain date years to valid years that we want to count
file['date'] = np.where(file['date'] == '05/11/1982', '05/11/2013',
                        np.where(file['date'] == '06/11/1948', '06/11/2016',
                                 np.where(file['date'] == '12/01/2064', '12/01/2014',
                                          np.where(file['date'] == '01/21/1942', '01/21/2015',
                                                   np.where(file['date'] == '07/25/2035', '07/25/2017',
                                                            np.where(file['date'] == '07/08/2042', '07/05/2018',
                                                                     file['date']))))))

# copy the file onto itself 17X
for i in range(17):
    new = file.copy(deep=True)
    file = file.append(new, ignore_index=True)

# limit file to one million records
file = file[:1000000]

# add unique id
file['guid'] = file.index

mega = file.to_csv(Path.cwd().with_name('data') / "mega.csv")

runtime = datetime.now() - startTime

print(f'Runtime is: {runtime}')

gc.collect()
