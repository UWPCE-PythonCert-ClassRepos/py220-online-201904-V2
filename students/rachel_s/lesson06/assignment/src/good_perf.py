import uuid
import timeit
import cProfile
import csv
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
    '''
    Takes a path to an existing data set in CSV format.
    Returns a list of lists with the items from that data set.
    '''
    data = []
    with open(path, newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for line in reader:
            data.append(line)
    # Remove the headers, we do not want them.
    del data[0]
    return data


def records_csv(num_records, path):
    '''
    Duplicates the data found in get_data_to_repro() and saves it to a
    file. You can specify how many duplicate records to create.
    '''
    with open(path, 'w') as file:
        file.write('seq,guid,seq,seq,ccnumber,date,sentence\n')
        seq = 0
        record_count = 0
        records = get_data_to_repro('../data/exercise.csv')
        max_seq = len(records) - 1
        while record_count < num_records:
            my_record = records[seq]
            my_record[1] = str(uuid.uuid4())
            file.write(','.join(my_record) + '\n')
            record_count += 1
            if seq < max_seq:
                seq += 1
            else:
                seq = 0



# Okay how long does it take though?
if __name__ == "__main__":
    records_csv(2000, 'twothousand.csv')

