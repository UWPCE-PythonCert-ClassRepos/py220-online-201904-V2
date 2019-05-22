"""
check good works the same, and is faster
"""
import pytest
import src.poor_perf as p
import src.good_perf as g
import pathlib
import os
ASSIGNMENT_FOLDER = pathlib.Path(__file__).parents[1]
CSV_FILE = ASSIGNMENT_FOLDER / "data/exercise.csv"



def test_assess_preformance():
    """ compare """
    poor = p.analyze(CSV_FILE)
    good = g.analyze(CSV_FILE)
    poor_elapsed = poor[1] - poor[0]
    good_elapsed = good[1] - good[0]
    assert good_elapsed < poor_elapsed
    assert poor[2] == good[2]
    assert poor[3] == good[3]
