#!/usr/bin/env python3
""""
must use 127.0.0.1 on windows
pip install pymongo

"""

import pprint
import json
from loguru import logger as log


cd_ip_one = {"artist": "The Who", "Title": "By Numbers"}

cd_ip_many = [
            {"artist": "Deep Purple", "Title": "Made In Japan", "name": "Andy"},
            {"artist": "Led Zeppelin", "Title": "House of the Holy", "name": "Andy"},
            {"artist": "Pink Floyd", "Title": "DSOM", "name": "Andy"},
            {"artist": "Albert Hammond", "Title": "Free Electric Band", "name": "Sam"},
            {"artist": "Nilsson", "Title": "Without You", "name": "Sam"},
]

collector_ip = [
            {"name": "Andy", "preference": "Rock"},
            {"name": "Sam", "preference": "Pop"},
]


def write_json_file(content, filename):
    with open(filename, 'w') as json_file:
        log.info("Writing contents to json file")
        pprint.pprint(content)
        json.dump(content, json_file)
        log.info("Closing json_file")
        json_file.close()


def main():

    write_json_file(cd_ip_many, 'cd_ip_many.json')
    write_json_file(cd_ip_one, 'cd_ip_one.json')
    write_json_file(collector_ip, 'collector_ip.json')


if __name__ == "__main__":
    main()
