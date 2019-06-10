"""
lesson 09
"""
import sys
import os
#pylint: disable=R1710

def png_recursion(folder):
    """
    method to look in folder, add all files then head to next folder
    ex: path_list = [folder,file1,file2,subfolder,file3,file4,subsubfolder,file1]
    """
    if folder == "images":
        start_path = os.getcwd() + "/" + folder
        file_list = []
        all_files = []
        return_list = []
        # for root, directories, files in os.walk(start_path):

        for dirpath, dirnames, filenames in os.walk(start_path):

            file_list = []
            for file in filenames:
                if file.endswith('.png'):
                    file_list.append(file)
                    all_files.append(filenames)

            if file_list:
                return_list.append(dirpath)
                return_list.append(file_list)

            if dirnames:
                for folders in dirnames:
                    png_recursion(folders)
        return all_files


if __name__ == "__main__":
    # sys.argv.append(1)
    OUTPUT = png_recursion(str(sys.argv[1]))
    print(OUTPUT)
