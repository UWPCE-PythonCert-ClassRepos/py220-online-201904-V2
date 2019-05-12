#!/usr/bin/env python3

""" Calls the cythonized program """

# pylint: disable=E0401, E0611
from poor_perf_v15 import analyze


if __name__ == "__main__":
    # Loop was used to run the program multiple times for better results on
    #   a higher-performing system.  A single test of say .5 sec was less
    #   reliable than 10 tests at 4.95 seconds.  Reset to 1 loop for submission
    #   in case grading is done on a potato.
    for loop in range(1):
        print(f"loop : {loop}")
        analyze("data/dataset.csv")
