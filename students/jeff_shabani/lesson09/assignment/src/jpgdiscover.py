from loguru import logger
import os
import pathlib

DATA_PATH = pathlib.Path.cwd().with_name('data')

for _, dirs, fils in os.walk(DATA_PATH):
    print(f'{fils} und {dirs}')
