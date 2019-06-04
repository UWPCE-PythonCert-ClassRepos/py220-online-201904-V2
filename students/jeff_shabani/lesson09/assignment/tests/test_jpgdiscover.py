"""
grade l9 part 3
"""
from jpgdiscover import *
from pathlib import Path
import pytest
import unittest

DATA_PATH = Path.cwd().with_name('data')

TEST_DATA = [['C:\\JRS\\Python\\py220\\students\\jeff_shabani\\lesson09\\assignment\\data\\furniture\\chair',
              ['metal_chair_back_isometric_400_clr_17527.png']],
             ['C:\\JRS\\Python\\py220\\students\\jeff_shabani\\lesson09\\assignment\\data\\furniture\\chair\\couch',
              ['sofa_400_clr_10056.png']],
             ['C:\\JRS\\Python\\py220\\students\\jeff_shabani\\lesson09\\assignment\\data\\furniture\\table',
              ['basic_desk_main_400_clr_17523.png',
               'desk_isometric_back_400_clr_17524.png', 'table_with_cloth_400_clr_10664.png']],
             ['C:\\JRS\\Python\\py220\\students\\jeff_shabani\\lesson09\\assignment\\data\\new',
              ['chairs_balancing_stacked_400_clr_11525.png',
               'hotel_room_400_clr_12721.png']],
             ['C:\\JRS\\Python\\py220\\students\\jeff_shabani\\lesson09\\assignment\\data\\old',
              ['couple_on_swing_bench_400_clr_12844.png', 'sitting_in_chair_relaxing_400_clr_6028.png']]]


class JPGDiscoverTesting(unittest.TestCase):

    def test_list_jpg_files(self):
        expected = TEST_DATA
        self.assertEqual(expected, list_jpg_files(DATA_PATH))


if __name__ == '__main__':
    unittest.main()
