"""
Search for jpg files
"""
import argparse
import os


def parse_cmd_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Find JPG files recursively in a directory.')
    parser.add_argument(
        '-d', '--directory', help='directory in which to find JPG files', required=True)
    return parser.parse_args()


def search_for_jpg_files(directory, master_files):
    """
    Append found jpg files to directory
    """
    entries = os.listdir(directory)
    files_found_in_current_directory = []
    for e in entries:
        if os.path.isdir(os.path.join(directory, e)):
            search_for_jpg_files(os.path.join(directory, e), master_files)
        elif os.path.isfile(os.path.join(directory, e)) and e.upper().endswith('.JPG'):
            files_found_in_current_directory.append(e)
    master_files.append(directory)
    master_files.append(files_found_in_current_directory)


def main(directory):
    """
    Print jpg findings
    """
    print('Directory: %s' % directory)
    files = []
    search_for_jpg_files(directory, files)
    print('JPG Files Found:')
    print(files)


if __name__ == '__main__':

    main(parse_cmd_args().directory)
