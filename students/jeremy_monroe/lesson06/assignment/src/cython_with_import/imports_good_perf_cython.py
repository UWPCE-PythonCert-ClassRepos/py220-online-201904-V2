"""
An attempt at using cython as an import rather than through the typical build
process.
"""

import pyximport
import good_perf_cython

pyximport.install()


def main(filename):
    """ To be run if __name__ == __main__ """
    result = good_perf_cython.main(filename)
    print(len(result))


if __name__ == '__main__':
    main('data/exercise.csv')
