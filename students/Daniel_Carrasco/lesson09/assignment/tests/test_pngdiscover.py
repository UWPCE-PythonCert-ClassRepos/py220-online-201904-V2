"""
grade l9 part 3
"""
import pytest

import pngdiscovery as sut

@pytest.fixture
def _test_list_jpg_files():
    """ structure from test """
    return  [
        ['sitting_in_chair_relaxing_400_clr_6028.png', 'couple_on_swing_bench_400_clr_12844.png'],
        ['sitting_in_chair_relaxing_400_clr_6028.png', 'couple_on_swing_bench_400_clr_12844.png'],
        ['metal_chair_back_isometric_400_clr_17527.png'],
        ['sofa_400_clr_10056.png'],
        ['table_with_cloth_400_clr_10664.png', 'basic_desk_main_400_clr_17523.png', 'desk_isometric_back_400_clr_17524.png'],
        ['table_with_cloth_400_clr_10664.png', 'basic_desk_main_400_clr_17523.png', 'desk_isometric_back_400_clr_17524.png'],
        ['table_with_cloth_400_clr_10664.png', 'basic_desk_main_400_clr_17523.png', 'desk_isometric_back_400_clr_17524.png'],
        ['chairs_balancing_stacked_400_clr_11525.png', 'hotel_room_400_clr_12721.png'], ['chairs_balancing_stacked_400_clr_11525.png', 'hotel_room_400_clr_12721.png']
        ]

def test_png_recursion(_test_list_jpg_files):
    """ student geneartes """
    all_files = sut.png_recursion("images")
    print(all_files)
    result =  all(elem in all_files  for elem in _test_list_jpg_files)
    assert result == True
