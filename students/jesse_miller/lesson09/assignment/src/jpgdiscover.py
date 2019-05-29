'''
Lesson 09 Assignment - Part 3
Recursion
'''

import os

def jpg_discover(directory, jpg_list=None):
    '''
    Recursively searches a parent directory and all subdirectories for jpg files.
    '''

    if jpg_list is None:
        jpg_list = []

    current_list = [directory, []]

    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            jpg_discover(os.path.join(directory, item), jpg_list)

        if item.endswith('.jpg'):
            current_list[1].append(item)

    if current_list[1]:  # Check if there are jpg files in current_list.
        jpg_list.extend(current_list)

    return jpg_list


print('List of directories with jpg files:')

IMAGE_LIST = jpg_discover(os.path.join(os.getcwd(), 'data'))

for sublist in IMAGE_LIST:
    print(sublist)
