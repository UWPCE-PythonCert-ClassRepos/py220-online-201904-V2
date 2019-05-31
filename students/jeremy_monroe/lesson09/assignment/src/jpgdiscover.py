""" Jeremy Monroe Assignment 09 """

import os
import argparse


def parse_cmd_arguments():
    """ Parses arguments entered at the command line. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filetype', nargs='?', const=1,
                        help=("Enter the filetype to"
                              " search for. Ex: '.jpg'"), default='.jpg')

    return parser.parse_args()


def list_jpg_files(dir_name):
    """
    Takes a directory name and finds all jpg files within said directory and
    any subdirectories.
    """
    jpg_list = []

    for item in os.walk(dir_name):
        temp_jpg_list = []
        for filename in item[2]:
            if FILETYPE in filename.lower():
                temp_jpg_list.append(filename)
        if temp_jpg_list:
            jpg_list.append(item[0])
            jpg_list.append(temp_jpg_list)

    return jpg_list


if __name__ == '__main__':
    FILETYPE = parse_cmd_arguments().filetype
    print(list_jpg_files('../data/'))

    # print(f"Printing jpg_list {jpg_list}")
