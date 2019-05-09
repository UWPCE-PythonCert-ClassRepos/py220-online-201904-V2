#!/usr/bin/env python3

""" Calls the cythonized program """

#pylint: disable=E0401, E0611
from poor_perf_v15 import analyze


if __name__ == "__main__":
    for loop in range(100):
        print(f"loop : {loop}")
        analyze("data/dataset.csv")
