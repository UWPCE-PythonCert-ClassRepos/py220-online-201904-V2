#!/usr/bin/env python3
"""
map, filter and reduce

"""

#import pytest

def test_map():
    # apply an operation to each member of a sequence

    items = [1, 2, 3, 4, 5]
    squared = []
    for x in items:
        squared.append(x ** 2)

    assert squared == [1, 4, 9, 16, 25]

    #-------------------------------------------------------------------------

    # OR:

    items = [1, 2, 3, 4, 5]
    def sqr(x): return x ** 2
    squared = list(map(sqr, items))  # map() returns a map object

    assert squared == [1, 4, 9, 16, 25]

    #-------------------------------------------------------------------------

    # how about:
    items = [1, 2, 3, 4, 5]
    squared = list(map((lambda x: x ** 2), items))

    assert squared == [1, 4, 9, 16, 25]

    # so generally, map(a_function, a_sequence)
    # BUT: does a_sequence have to be "values"???

    #-------------------------------------------------------------------------

    # cool stuff:

    def square(x):
        return x**2

    def cube(x):
        return x**3

    funcs = [square, cube]
    output = []
    for r in range(5):
        value = list(map(lambda x: x(r), funcs))
        output.append(value)

    assert output == [[0, 0], [1, 1], [4, 8], [9, 27], [16, 64]]

    # note: map can be faster than the manually coded equivalent for loop...

    #-------------------------------------------------------------------------

    # using multiple sequence p[arameters in parallel

    assert pow(2, 10) == 1024
    assert pow(3, 11) == 177147
    assert pow(4, 12) == 16777216
    assert list(map(pow, [2, 3, 4], [10, 11, 12])) == [1024, 177147, 16777216]

    #-------------------------------------------------------------------------

    from operator import add

    x = [1, 2, 3]
    y = [4, 5, 6]

    assert list(map(add, x, y)) == [5, 7, 9]

    #-------------------------------------------------------------------------

    """
    The map call is similar to the list comprehension expression.
    But map applies a function call to each item instead of an arbitrary expression.
    Because of this limitation, it is somewhat less general tool.
    In some cases, however, map may be faster to run than a list comprehension
    such as when mapping a built-in function. And map requires less coding.
    """

    # An identity function takes a single argument and returns it unchanged:

    x = 1

    def func(x):
        return x

    assert func(x) == x

    assert lambda x: x == x

    #-------------------------------------------------------------------------

    m = [1, 2, 3]
    n = [1, 4, 9]

    new_tuples = list(map(lambda x, y: (x, y), m, n))

    assert new_tuples == [(1, 1), (2, 4), (3, 9)]

    # but better:

    assert list(zip(m, n)) == [(1, 1), (2, 4), (3, 9)]

    #-------------------------------------------------------------------------

    m = [1, 2, 3]
    n = [1, 4, 9, 10]

    assert list(zip(m, n)) == [(1, 1), (2, 4), (3, 9)]  # !!!!

    # prehaps use

    from itertools import zip_longest
    assert list(zip_longest(m, n)) == [(1, 1), (2, 4), (3, 9), (None, 10)]

    #-------------------------------------------------------------------------


def test_reduce():
    """
    reduce is in functools It is more complex. It accepts an iterator to process,
    but it's not an iterator itself. It returns a single result.

    Coded longhand:

    """
    l = [1, 2, 3, 4]
    result = l[0]

    for x in l[1:]:
        result = result * x

    assert result == 24

    result = l[0]
    for x in l[1:]:
        result = result / x

    assert result == 0.041666666666666664

    #-------------------------------------------------------------------------
    # use reduce

    from functools import reduce

    assert reduce((lambda x, y: x * y), [1, 2, 3, 4]) == 24
    assert reduce((lambda x, y: x / y), [1, 2, 3, 4]) == 0.041666666666666664

    #-------------------------------------------------------------------------
    # strings too

    l = ['I ', 'passed ', 'the ', 'Python ', 'certificate']
    assert reduce((lambda x, y: x + y), l) == 'I passed the Python certificate'


def test_filter():

    assert list(range(-5, 5)) == [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
    assert list(filter((lambda x: x < 0), range(-5, 5))
                ) == [-5, -4, -3, -2, -1]
    # Items in the sequence or iterable for which the function returns a true,
    # the result are added to the result list. Built in and fast

    #-------------------------------------------------------------------------

    a = [1, 2, 3, 5, 7, 9]
    b = [2, 3, 5, 6, 7, 8]
    assert list(filter(lambda x: x in a, b)) == [2, 3, 5, 7]

    #-------------------------------------------------------------------------

    # but perhaps a compoprehension instead
    a = [1, 2, 3, 5, 7, 9]
    b = [2, 3, 5, 6, 7, 8]
    assert [x for x in a if x in b] == [2, 3, 5, 7]

    #-------------------------------------------------------------------------


if __name__ == "__main__":
    test_map()
    test_reduce()
    test_filter()
