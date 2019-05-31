"""
grade l9 part 3
"""
import pytest

import jpgdiscover as sut

@pytest.fixture
def _test_list_jpg_files():
    """ structure from test """
    return  [
        ['../data/', '76-2.jpg']
        ]

def test_list_jpg_files(_test_list_jpg_files):
    """ student geneartes """
    jpgs = sut.list_jpg_files("../data/")
    assert jpgs == _test_list_jpg_files
