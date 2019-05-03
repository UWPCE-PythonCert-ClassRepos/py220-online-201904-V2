#!/usr/bin/env python3

import json
from pymongo import MongoClient
from loguru import logger as log


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


def read_json_file(filename):
    with open(filename) as content:
        return json.load(content)


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)


def reset_db(cd, collector):
    # start afresh next time?
    yorn = input("Drop data?")
    if yorn.upper() == "Y":
        cd.drop()
        collector.drop()


def main():
    mongo = MongoDBConnection()

    with mongo:
        log.info("Initializing database...")
        db = mongo.connection.media

        log.info("Creating CD collection")
        cd = db["cd"]
        log.info("Reading data/cd_ip_one.json into mongodb...")
        cd_ip_one = read_json_file('data/cd_ip_one.json')
        cd.insert_one(cd_ip_one)
        print_mdb_collection(cd)
        log.info("Reading data/cd_ip_many.json into mongodb...")
        cd_ip_many = read_json_file('data/cd_ip_many.json')
        cd.insert_many(cd_ip_many)
        print_mdb_collection(cd)

        collector = db["collector"]
        log.info("Reading data/collector_ip.json into mongodb...")
        collector_ip = read_json_file('data/collector_ip.json')
        collector.insert_many(collector_ip)
        print_mdb_collection(collector)

        reset_db(cd, collector)


if __name__ == "__main__":
    main()
