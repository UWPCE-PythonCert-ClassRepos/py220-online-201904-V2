import csv
import functools
import gc
import numpy as np
import pandas as pd
from pathlib import Path
import timeit

from lesson06.assignment.src.dekor import timer

pd.options.display.float_format = '{:0,.2f}'.format
pd.set_option('display.max.columns', 25)
desired_width = 400
pd.set_option('display.width', desired_width)

read = pd.read_csv

#@functools.lru_cache()
#@timer
new='''
def importer():
    file = read(Path.cwd().with_name('data') / "exercise.csv")
    # file = pd.DataFrame(file)
    # new = file.copy(deep=True)
    # file = file.append(new)
    return file
'''

#@timer
old='''
def old():
    src = Path.cwd().with_name('data') / "exercise.csv"
    with open(src) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        return reader
'''


new_times=timeit.timeit(new, number=1000000)
old_times=timeit.timeit(old, number=1000000)
print(f'Pandas {new_times:,.8f}')
print(f'Non-pandas {old_times:,.8f}')



#print(importer())

gc.collect()