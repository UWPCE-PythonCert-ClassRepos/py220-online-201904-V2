import random
import logging
import concurrent.futures
import queue
import os
import hashlib
import csv
import string
import datetime
import pathlib
from threading import Event

HEADER = ["seq", "guid", "seq", "seq", "ccumber", "date", "sentence"]
ASSIGNMENT_FOLDER = pathlib.Path(__file__).parents[1]
CSV_FILE = ASSIGNMENT_FOLDER / "data/exercise.csv"
CSV_FILE = open(CSV_FILE, "w", newline='')
CSV_WRITER = csv.writer(CSV_FILE, delimiter=",")
CSV_WRITER.writerow(HEADER)
D1 = datetime.datetime.strptime('1/1/1900', '%m/%d/%Y')
D2 = datetime.datetime.strptime('1/1/2100', '%m/%d/%Y')
DELTA = (D2 - D1).days


def producer(pipeline, event):
    """" create 1000,000 records as generator"""
    for i in range(1000000):
        guid = hashlib.md5(os.urandom(32)).hexdigest()
        guid = "-".join([guid[:7], guid[7:11], guid[11:15], guid[15:19], guid[19:]])
        ccnumber = random.randrange(1e14, 1e16)
        random_days = random.randrange(DELTA)
        date = D1 + datetime.timedelta(days=random_days)
        date = date.strftime('%m/%d/%Y')
        sentence = random.choice(string.ascii_uppercase) + " ".join(
            ("".join(random.choices(string.ascii_lowercase, k=random.randrange(2, 7))) for j in
             range(random.randrange(1, 20))))
        pipeline.put((i + 1, guid, i + 1, i + 1, ccnumber, date, sentence))
    event.set()


def consumer(pipeline, event):
    while not event.is_set() or not pipeline.empty():
        item = pipeline.get(timeout=0.01)
        CSV_WRITER.writerow(item)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    pipeline = queue.Queue()
    event = Event()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)
