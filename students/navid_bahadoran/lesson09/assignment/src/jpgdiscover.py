# pylint: disable = W0703, C0301, W0611
""" this program ask for the parent directory and the file suffix in the command line, then return
list of file in each directory that has the same suffix as given """
import argparse
import os
import pathlib
import pprint


# PARSER = argparse.ArgumentParser(description="Finding JPG files!")
# PARSER.add_argument('-p', '--parent', help="need to enter the path", required=True)
# PARSER.add_argument('-s', '--suffix', help='for entering the file suffix', default='.png')
# ARGS = PARSER.parse_args()


def finding_files_with_os_walk(directory):
    """ find the files with the given suffix with os.walk method from os module"""
    total_list = []
    for paths, _, files in os.walk(directory):
        file_list = []
        for file in files:
            if os.path.splitext(file)[1] == '.png':
                file_list.append(file)
        total_list.append(paths)
        total_list.append(file_list)
    return total_list


SUFFIX_LIST = []


def list_jpg_files(directory):
    """ find the file with the suffix with recursive function"""
    file_list = []
    folder = set()
    for i in directory.iterdir():
        if i.suffix == ".png":
            folder.add(i.parent)
            file_list.append(i.name)
    if file_list:
        SUFFIX_LIST.append(folder.pop())
        SUFFIX_LIST.append(file_list)
    for i in directory.iterdir():
        if i.is_dir():
            list_jpg_files(i)
    return SUFFIX_LIST
