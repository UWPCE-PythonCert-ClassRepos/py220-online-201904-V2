# pylint: disable =  W0703, C0301
""" craeate ..."""

import csv
import logging
import os
import pathlib
from functools import partial

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
CONSOLE = logging.StreamHandler()
CONSOLE.setFormatter(FORMATTER)
CONSOLE.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE)

DATA_DIR = pathlib.Path(os.path.abspath(__file__)).parents[1] / "data"


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ add furniture to csv file"""
    try:
        invoice_file_path = os.path.join(DATA_DIR, invoice_file)
        file_handler = open(invoice_file_path, newline='', mode='a')
        header = ("customer_name", "item_code", "item_description", "item_monthly_price")
        csv_writer = csv.DictWriter(file_handler, fieldnames=header)
        # write header only when the file is empty
        if os.stat(invoice_file_path).st_size == 0:
            csv_writer.writeheader()
        new_line = dict(zip(header, (customer_name, item_code, item_description, item_monthly_price)))
        csv_writer.writerow(new_line)
    except Exception:
        LOGGER.debug("There is an issue in opening the file!")
    finally:
        file_handler.close()


def single_customer(customer_name, invoice_file):
    """ create a single customer closure"""
    add_item_for_single_customer = partial(add_furniture, invoice_file, customer_name)

    def read_rental(rented_file):
        """ add items in rented file and assign it to the single customer and write it to invoice file"""
        try:
            rented_file_path = os.path.join(DATA_DIR, rented_file)
            rented_handler = open(rented_file_path, newline='', mode='r')
            header = ("item_code", "item_description", "item_monthly_price")
            rented_reader = csv.DictReader(rented_handler, fieldnames=header)
            for item in rented_reader:
                if item:
                    add_item_for_single_customer(**item)
                else:
                    continue
        except Exception:
            LOGGER.debug("There is an issue in opening file!")
        finally:
            rented_handler.close()

    return read_rental


def read_csv(file_name):
    """ red the csv file and return it in dictionary"""
    try:
        file_path = os.path.join(DATA_DIR, file_name)
        file_handler = open(file_path, mode='r', newline='')
        csv_reader = csv.DictReader(file_handler)
        return csv_reader
    except Exception:
        LOGGER.debug("There is an issue in opening the file")
    # finally:
    #     file_handler.close()


def clean_file(file_name):
    """ clean the existing file"""
    file_path = os.path.join(DATA_DIR, file_name)
    open(file_path, mode='w').close()


# add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
# add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
# add_furniture("rented_items.csv", "Alex Gonzales", "QM78", "Queen Mattress", 17)
# create_invoice = single_customer("Susan Wong", "rented_items.csv")
# create_invoice("test_items.csv")
