"""
Module that returns a list of image directories containing
files of a specified type.
"""
import argparse
import os
import pathlib

DATA_PATH = pathlib.Path.cwd().with_name('data')
RESULT = []


def parse_cmd_arguments():
    """
    parses command line arguments entered for debug level, source file name,
    and output file name.
    :return: arguments entered at command line
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-p', '--path', type=str, required=True,
                        metavar='', help='Path to iterate over', default=1)
    args = parser.parse_args()
    return args


def list_jpg_files(path_: str):
    """
    User creates list of directory containing files
    of a specific type
    :param path_:
    :return: list of lists
    """
    for i in os.walk(path_):
        final_result = []
        for _f in i[-1]:
            if 'png' in _f:
                k = i[0], i[-1]
                RESULT.append(k)

        for item in RESULT:
            if list(item) not in final_result:
                final_result.append(list(item))
    return final_result


if __name__ == '__main__':
    INARGS = parse_cmd_arguments()
    print(list_jpg_files(INARGS.path))
