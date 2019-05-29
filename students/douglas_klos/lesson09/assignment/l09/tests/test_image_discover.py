"""
grade l9 part 3
"""


from pytest import fixture
import src.image_discover as img


@fixture
def _test_list_image_files():
    """ structure from test """

    return [
        "data/new",
        [
            "chairs_balancing_stacked_400_clr_11525.png",
            "hotel_room_400_clr_12721.png",
        ],
        "data/furniture/table",
        [
            "desk_isometric_back_400_clr_17524.png",
            "basic_desk_main_400_clr_17523.png",
            "table_with_cloth_400_clr_10664.png",
        ],
        "data/furniture/chair/couch",
        ["sofa_400_clr_10056.png"],
        "data/furniture/chair",
        ["metal_chair_back_isometric_400_clr_17527.png"],
        "data/old",
        [
            "couple_on_swing_bench_400_clr_12844.png",
            "sitting_in_chair_relaxing_400_clr_6028.png",
        ],
    ]


def test_list_image_files(_test_list_image_files):
    """ student geneartes """
    images = img.list_image_files("./data/")
    assert images == _test_list_image_files
