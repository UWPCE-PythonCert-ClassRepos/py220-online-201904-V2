import pyximport; pyximport.install()
import good_perf_cython


def main(filename):
    result = good_perf_cython.main(filename)
    print(len(result))


if __name__ == '__main__':
    main('data/exercise.csv')
