"""
This module takes original exercise file and creates a
new file with 1,000,000 records.
"""

from datetime import datetime
import gc
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

for i in range(17):
    new = file.copy(deep=True)
    file = file.append(new, ignore_index=True)
file = file[:1000000]
# file['guid'] = range(len(file))
file['guid'] = file.index

mega = file.to_csv(Path.cwd().with_name('data') / "mega.csv")

runtime = datetime.now() - startTime

print(f'Runtime is: {runtime}')

gc.collect()
