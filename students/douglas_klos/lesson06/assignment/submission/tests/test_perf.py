"""
check good works the same, and is faster
"""

import src.poor_perf_v00 as p
import src.poor_perf_v15 as g


def test_assess_preformance():
    """ compare """
    poor = p.analyze('data/dataset.csv')
    good = g.analyze('data/dataset.csv')
    poor_elapsed = poor[1] - poor[0]
    good_elapsed = good[1] - good[0]
    assert good_elapsed < poor_elapsed
    assert poor[2] == good[2]
    assert poor[3] == good[3]
