'''
expand records to one million records and assign unique id to them
'''
import logging
import csv
import uuid
import random

#global CCNUMBER_LIST, DATA_LIST, SENTENCE_LIST

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def read_csv(filename):
    '''read data from csv'''
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        old_record = []
        ccnumber_list = []
        date_list = []
        sentence_list = []
        for i, row in enumerate(reader):
            lrow = list(row)
            old_record.append(lrow)
            #collecting data pool for expansion
            if i > 1:
                ccnumber_list.append(lrow[4])
                date_list.append(lrow[5])
                sentence_list.append(lrow[6])
        #LOGGER.info('csv contains %s', new_ones)
        #LOGGER.info('date_list %s', date_list)
    return old_record, ccnumber_list, date_list, sentence_list


def generate(num1, num2):
    '''generate up to 1,000,000 records'''
    new_record = list(map(create_entry, range(num1, num2)))

    #alternative way
    #new_record = []
    #for i in range(num1, num2): #1,000,000
        #guid = str(uuid.uuid4())
        #randomly select from ccnumber, date and sentence pool
        #ccnumber = random.choice(ccnumber_list)
        #date = random.choice(date_list)
        #sentence = random.choice(sentence_list)
        #row = [i, guid, i, i, ccnumber, date, sentence]
        #new_record.append(row)
    #LOGGER.info('expanded record is %s', new_record)
    return new_record


def create_entry(index):
    '''create an entry row, called by map function'''
    guid = str(uuid.uuid4())
    ccnumber = random.choice(CCNUMBER_LIST)
    date = random.choice(DATE_LIST)
    sentence = random.choice(SENTENCE_LIST)
    return [index, guid, index, index, ccnumber, date, sentence]


def write_to_csv(filename, data):
    '''write data to csv'''
    with open(filename, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerows(data)


if __name__ == "__main__":
    INPUT_FILENAME = "../data/exercise.csv"
    ORIGINAL_DATA, CCNUMBER_LIST, DATE_LIST, SENTENCE_LIST = \
        read_csv(INPUT_FILENAME)
    EXPANDED_DATA = generate(10, 1000001)
    OUTPUT_FILENAME = "../data/exercise2.csv"
    DATA = ORIGINAL_DATA + EXPANDED_DATA
    write_to_csv(OUTPUT_FILENAME, DATA)
