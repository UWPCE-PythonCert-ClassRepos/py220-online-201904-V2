import uuid
import timeit
import cProfile
import pandas as pd
from loguru import logger


# This is cool but also takes way too long because Faker is slow so
# we're not gonna do it but I am saving it for posterity.
#
# def make_record(seq):
#     '''
#     Makes a single record with fake data in the following format:
#     seq, guid, seq, seq, ccnumber, date, sentence
#     '''
#     seq = str(seq)
#     fake = faker.Faker()
#     return(','.join([
#         seq,
#         str(uuid.uuid4()),
#         seq,
#         seq,
#         str(random.randint(1000000000000000, 9999999999999999)),
#         fake.date(pattern="%m/%d/%Y", end_datetime=None),
#         fake.sentence(nb_words=random.randint(10,20))
#         ]))

def get_data_to_repro(path):
    pass


def records_csv(num_records, path):
    '''
    Makes a CSV file with the specified number of records using the 
    make_record function. Saves it to the specified path.
    '''
    with open(path, 'w') as file:
        file.write('seq,guid,seq,seq,ccnumber,date,sentence\n')
        seq = 1
        while seq <= num_records:
            my_seq = str(seq)
            my_record = ([
                my_seq,

            ])
            file.write(my_record + '\n')
            seq += 1

# Okay how long does it take though?
if __name__ == "__main__":
    records_csv(2000, 'twothousand.csv')

