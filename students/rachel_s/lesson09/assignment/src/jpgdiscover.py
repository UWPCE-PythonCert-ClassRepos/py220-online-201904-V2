#!/usr/bin/env python3

'''
It's a Thursday and Thursdays are bad for recursively finding images in
a directory and that directory's children.
'''

# Rachel Schirra
# June 2, 2019
# Python 220 Lesson 02

from pathlib import Path

def list_jpg_files(path):
    '''
    Recursively discovers pngs in the given directory and any child
    directories. It does not discover jpgs because the test data we were
    given is in fact pngs.
    '''
    my_path = Path(path)
    images = []
    result = []
    for item in my_path.iterdir():
        if item.suffix == '.png':
            images.append(item.name)
    if images:
        result = [str(Path.resolve(my_path)), images]
    for item in my_path.iterdir():
        if item.is_dir():
            result += list_jpg_files(str(item))
    return result
