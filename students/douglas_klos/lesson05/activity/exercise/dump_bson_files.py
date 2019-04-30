#!/usr/bin/env python3
""""
must use 127.0.0.1 on windows
pip install pymongo

"""

import json
import pprint
from pymongo import MongoClient
from loguru import logger as log
from bson import json_util
import bson

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


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host="127.0.0.1", port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)


def write_json_file(content, filename):
    with open(filename, 'w') as json_file:
        log.info("Writing contents to json file")
        pprint.pprint(content)
        json.dump(content, json_file)
        log.info("Closing json_file")
        json_file.close()


def read_json_file(filename):
    with open(filename, 'r') as json_file:
        log.info(f"Reading contents of json file {filename}...")
        return(json.load(json_file))


def reset_db(cd, collector):
    # start afresh next time?
    yorn = input("Drop data?")
    if yorn.upper() == "Y":
        cd.drop()
        collector.drop()


def display_related_data(cd, collector):
    # related data
    for name in collector.find():
        print(f'List for {name["name"]}')
        query = {"name": name["name"]}
        for a_cd in cd.find(query):
            print(f'{name["name"]} has collected {a_cd}')


def main():
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.media

        # collection in database
        cd = db["cd"]
        cd.insert_one(cd_ip_one)
        cd.insert_many(cd_ip_many)
        print_mdb_collection(cd)

        # another collection
        collector = db["collector"]
        collector.insert_many(collector_ip)
        print_mdb_collection(collector)

        write_json_file(json_util.dumps(cd_ip_one), 'cd_ip_one.bson')
        write_json_file(json_util.dumps(cd_ip_many), 'cd_ip_many.bson')
        write_json_file(json_util.dumps(collector_ip), 'collector_ip.bson')

        display_related_data(cd, collector)
        reset_db(cd, collector)


if __name__ == "__main__":
    main()
