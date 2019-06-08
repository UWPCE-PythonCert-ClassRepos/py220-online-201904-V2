"""
grade l9 part 3
"""
import pytest
import pathlib

import src.jpgdiscover as sut


@pytest.fixture
def _test_list_jpg_files():
    """ structure from test """
    return [pathlib.Path(__file__).parent / "data/furniture/chair",
            ['metal_chair_back_isometric_400_clr_17527.png'],
            pathlib.Path(__file__).parent / "data/furniture/chair/couch",
            ['sofa_400_clr_10056.png'],
            pathlib.Path(__file__).parent / "data/furniture/table",
            ['basic_desk_main_400_clr_17523.png',
             'desk_isometric_back_400_clr_17524.png',
             'table_with_cloth_400_clr_10664.png'],
            pathlib.Path(__file__).parent / "data/new",
            ['chairs_balancing_stacked_400_clr_11525.png', 'hotel_room_400_clr_12721.png'],
            pathlib.Path(__file__).parent / "data/old",
            ['couple_on_swing_bench_400_clr_12844.png',
             'sitting_in_chair_relaxing_400_clr_6028.png']]


def test_list_jpg_files(_test_list_jpg_files):
    """ student geneartes """
    path = pathlib.Path(__file__).parent / "data"
    jpgs = sut.list_jpg_files(path)
    assert jpgs == _test_list_jpg_files
