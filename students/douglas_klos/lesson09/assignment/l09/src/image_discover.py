#!/usr/bin/env python3
""" HPNorton recursive search for image files """


from pathlib import Path
from pprint import pprint
from argparse import ArgumentParser
from loguru import logger


def list_image_files(location):
    """ Recursively lists all images file in directory and sub-directories

    Arguments:
        location {string} -- Location to search

    Returns:
        ['directory name', ['image1', 'image2', 'image3']]
    """
    valid_extensions = [".jpg", ".gif", ".png", ".bmp"]
    logger.info(f"Start of {location}")
    path = Path(location)

    return_list = []
    file_list = []

    for item in path.iterdir():
        if item.is_dir():
            return_list += list_image_files(item)

    for item in path.iterdir():
        if item.is_file():
            if item.name[-4:].lower() in valid_extensions:
                file_list.append(item.name)

    if file_list:
        return_list.append(str(path))
        return_list.append(file_list)

    logger.info(f"Returning from {location}")
    return return_list


def main(argv=None):
    """ Main function for searching for image files

    Keyword Arguments:
        argv {list} -- Command line arguments.
    """
    args = parse_cmd_arguments(argv)
    pprint(list_image_files(args.find))


def parse_cmd_arguments(args):
    """ Parses the command line arguments

    Arguments:
        args {list} -- argument list from command line

    Returns:
        ArgumentParser.parse_args
    """
    parser = ArgumentParser(description="HPNorton Find JPG Files")
    parser.add_argument(
        "--find",
        help="Show list of all JPG files",
        action="store",
        required=True,
        default=False,
    )
    return parser.parse_args(args)


if __name__ == "__main__":
    main()
