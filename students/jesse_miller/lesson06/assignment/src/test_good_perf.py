'''
Lesson 06 Assignment
Tests
'''

import good_perf as gp


def test_analyze():
    '''
    Makes sure that my refactored code still works properly.
    '''
    result = gp.analyze('exercise.csv')

    new_ones = {'2013': 8245, '2014': 8147, '2015': 8268, '2016': 8337, '2017': 8343, '2018': 8385}
    ao_total = 82515

    assert result[2] == new_ones
    assert result[3] == ao_total
