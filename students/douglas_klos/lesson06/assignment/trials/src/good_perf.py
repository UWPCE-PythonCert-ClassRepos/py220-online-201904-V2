#!/usr/bin/env python3
# pylint: disable= E0401
"""
This simply calls the current best performing
version of poor_perf.
"""

# from poor_perf_v15 import analyze
from poor_perf_v14 import analyze

if __name__ == "__main__":
    analyze("./data/dataset.csv")
