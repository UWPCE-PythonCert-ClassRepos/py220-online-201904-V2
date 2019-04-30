#!/usr/bin/env python3
'''
Mongo DB assignment for Python 220
'''
import csv
import os
import pymongo

class MongoDBConnection:
    '''
    Creating the connection to the Mongo daemon
    '''
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = pymongo.MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    '''
    Prints the documents in columns.  May address this later, may not
    '''
    for doc in collection_name.find():
        print(doc)


def _import_csv(filename):
    '''
    This returns a list of the stored dictionaries.  One per row.
    filename = .csv file
    return = list of dictionaries
    '''
    with open(filename, newline='') as csvfile:
        dict_list = []

        csv_data = csv.reader(csvfile)

        headers = next(csv_data, None)

    if headers[0].startswith("ï»¿"):  # Check for weird formatting
        headers[0] = headers[0][3:]

    for row in csv_data:
        row_dict = {}

        for index, column in enumerate(headers):
            row_dict[column] = row[index]

        dict_list.append(row_dict)
    return dict_list


def _add_bulk_data(collection, directory_name, filename):
    '''
    This, if it works properly, will handle the bulk imports from the csv
    files.
    '''
    file_path = os.path.join(directory_name, filename)

    try:
        collection.insert_many(_import_csv(file_path), ordered=False)
        return 0

    except pymongo.errors.BulkWriteError as bwe:
        print(bwe.details)
        return len(bwe.details["writeErrors"])
