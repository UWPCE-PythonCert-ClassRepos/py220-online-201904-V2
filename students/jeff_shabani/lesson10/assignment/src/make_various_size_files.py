"""
This module takes original exercise file and creates a
new file with 1,000,000 records.
"""

from datetime import datetime
import gc
import numpy as np
from pathlib import Path
import pandas as pd
import time

pd.options.display.float_format = '{:0,.2f}'.format
pd.set_option('display.max.columns', 25)
desired_width = 400
pd.set_option('display.width', desired_width)

read = pd.read_excel

file = pd.DataFrame(pd.read_csv(Path.cwd().with_name('data') / "customer.csv"))

for i in range(10):
    new = file.copy(deep=True)
    file = file.append(new, ignore_index=True)

# limit file to one million records
file = file[:100000]

# add unique id
file['guid'] = file.index

mega = file.to_csv(Path.cwd().with_name('data') / "customer_large.csv")

print(f'Runtime is: {time.process_time()}')

gc.collect()
