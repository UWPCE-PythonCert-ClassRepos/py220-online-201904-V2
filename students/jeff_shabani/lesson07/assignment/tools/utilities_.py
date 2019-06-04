#!/usr/bin/env python3

"""
Module that contains utility functions."""

import os
from pathlib import Path
from loguru import logger


def _delete_file_by_type(target_dir, file_ext):
    """
    Utility that removes all files in a directory by
    file type
    :param target_dir: directory containing files to delete
    :param file_ext: file extension to specify type i.e. '.json' for json
    :return:
    """
    os.chdir(target_dir)
    removal_path = Path.cwd()
    count = 0
    for _file in removal_path.iterdir():
        if _file.suffix == file_ext:
            logger.info(f'Removing {_file.name}.')
            count += 1
            os.remove(_file.name)
        if count == 0:
            logger.info(f'No files of type {file_ext} were found.')


if __name__ == '__main__':
    pass
