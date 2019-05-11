"""
    Create database examle with Peewee ORM, sqlite and Python
"""
# pylint: disable= W0614, W0106, W1203, E0602
import logging
import argparse
import basic_operations as bo

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)


def parse_cmd_arguments():
    """
    method to parse through cmd line agrument
    """
    logging.info('Start: parse_cmd_arguments()')
    parser = argparse.ArgumentParser(description='create database.')
    parser.add_argument(
        "-csv", "--csv", help="input csv name to create db", required=False)
    parser.add_argument("-print", "--print",
                        help="input csv name to create db", required=False)
    logging.info('End: parse_cmd_arguments()')
    logging.info(f'{parser.parse_args()}')
    return parser.parse_args()


def create_csvdb(csv):
    """
    method to create db from csv file
    """
    logging.info("creating db from csv file")
    database.create_tables([Customer])
    database.close()
    with open(csv, 'r', encoding='latin-1') as csvfile:
        customers = [row.split(',') for row in csvfile]

    [bo.add_customer(customer[0], customer[1], customer[2], customer[3], customer[4],
                     customer[5], customer[6], customer[7]) for customer in customers]
    return customers


def print_csvdb(csv):
    '''
    method to print csv data
    '''

    with open(csv, 'r', encoding='latin-1') as csvfile:
        customers = [row.split(',') for row in csvfile]
    [print(customer) for customer in customers[:10]]


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    if ARGS.csv:
        create_csvdb(ARGS.csv)
    else:
        logging.info('creating empty customer.db')
        database.create_tables([Customer])
        database.close()

    if ARGS.print:
        print_csvdb(ARGS.print)
