"""
Jeremy Monroe Assignment 09

I didn't quite meet the requirements for this one. I do use recursion to
analyze a list of files in order to determine their filetype. Unfortunately the
returned results do not meet the desired returned results.

In short I end up with lists within lists rather than just a list...

If you run this module directly from within the src directory the results will
be printed and you can see what I mean.
"""

import os
import argparse


def parse_cmd_arguments():
    """ Parses arguments entered at the command line. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filetype', nargs='?', const=1,
                        help=("Enter the filetype to"
                              " search for. Ex: '.jpg'"), default='.png')

    return parser.parse_args()


def list_jpg_files(dir_name):
    """
    Ok, list_jpg_files uses os.walk and a provided dir_name (directory name).
    The results are then passed into loop_directories and subsequently
    find_jpg_files to be processed in a recursive fashion.
    """
    files_and_dirs = list(os.walk(dir_name))
    # print(files_and_dirs)

    return loop_directories(files_and_dirs)


def loop_directories(files_and_dirs):
    """
    Takes a list of lists returned from os.walk, loops over those lists and
    passes relevant information (list of filenames) on to find_jpg_files for
    further analyzation.
    """
    jpg_dir_list = []
    # print("at top of loop directories")
    for directory in files_and_dirs:
        found_jpgs = [x for x in find_jpg_files(directory[2]) if x]

        if found_jpgs:
            jpg_dir_list.append(directory[0])
            jpg_dir_list.append(found_jpgs)

    return jpg_dir_list


def find_jpg_files(possible_files):
    """
    I wanted to implement recursive calls in loop_directories and here but
    wound up struggling quite a bit just to get it working here.

    Anyways, this takes a list and recursively analyzes its items to determine
    whether or not they ought to be returned.

    I never got this working in a way that will pass the provided tests. It
    does work, and does return consistent results, but I ran into a return issue
    where if the final else block is reached and '' is returned I end up with
    lists within lists, rather than the expected single list.

    I might clean that issue up after the fact when the list is returned to
    loop_directories.
    """
    # print("Top of find_jpg_files possible_files = {}".format(possible_files))
    if possible_files:
        if '.png' in possible_files[-1]:
            return [find_jpg_files(possible_files[:-1]), possible_files[-1]]
        else:
            return find_jpg_files(possible_files[:-1])
    else:
        return ''


def better_list_jpg_files(dir_name):
    """
    Does the same thing as list_jpg_files only it uses argparser to specify the
    file type to search for.

    ONLY works when __name__ == __main__

    This is me quite a bit later. This doesn't really do the same thing as
    list_jpg_files anymore. The results are similar but this one outputs what I
    was hoping to achieve with list_jpg_files. Unfortunately this function isn't
    recursive!!!
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

    # print(better_list_jpg_files('../data/'))

    print(list_jpg_files('../data/'))
    # list_jpg_files('../data/')
