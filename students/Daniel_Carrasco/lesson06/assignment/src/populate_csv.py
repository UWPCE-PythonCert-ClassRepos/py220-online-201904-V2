"""
moduel that will populate the csv to have 1,000,000 records
"""

import uuid # to make random guid
import csv
from faker import Faker

fake = Faker()
filename = "data/exercise.csv"

with open(filename,'r') as readfile:
    row_count = sum(1 for row in readfile)
print(row_count)


i = 0

while row_count - 1 < 1e6:
    new_seq = row_count + i
    new_guid = str(uuid.uuid4())
    new_date = str(fake.date(pattern="%Y-%m-%d", end_datetime=None))
    new_cc = fake.credit_card_number(card_type=None)
    new_sentence = fake.sentence()
    new_row = [new_seq, new_guid, new_seq, new_seq, new_cc, new_date, new_sentence]
    i+=1
    row_count +=1
    with open(filename,'a') as resultFile:
        wr = csv.writer(resultFile)
        wr.writerow(new_row)


