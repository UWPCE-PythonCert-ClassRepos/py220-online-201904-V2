"""his code creates a 1000,000 records in csv file named new_csv.csv"""
import os
import hashlib
import csv
import random
import string
import datetime

HEADER = ["seq", "guid", "seq", "seq", "ccumber", "date", "sentence"]
CSV_FILE = open("new_csv.csv", "w", newline='')
CSV_WRITER = csv.writer(CSV_FILE, delimiter=",")
CSV_WRITER.writerow(HEADER)
D1 = datetime.datetime.strptime('1/1/1900', '%m/%d/%Y')
D2 = datetime.datetime.strptime('1/1/2100', '%m/%d/%Y')
DELTA = (D2 - D1).days


def func():
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
        yield (i + 1, guid, i + 1, i + 1, ccnumber, date, sentence)


CSV_WRITER.writerows(func())
