"""
This program will find all the .png
files in the file directory system
"""

import os


def list_jpg_files(path):

    """This is the recursive function
       for discovering .png files"""

    path_list = []

    for root, directories, files in os.walk(path):

        file_list = []
        for file in files:

            if '.png' in file:

                file_list.append(file)

        if file_list != []:

            path_list.append(root)

            path_list.append(file_list)

        if directories:

            for directory in directories:

                list_jpg_files(directory)

    return path_list



if __name__ == '__main__':
    print(list_jpg_files(os.path.dirname(__file__)))


