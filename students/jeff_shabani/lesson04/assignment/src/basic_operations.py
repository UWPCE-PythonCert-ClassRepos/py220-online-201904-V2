#!/bin/python3

"""
This module reads in csv as pandas dataframe then creates a
table using that dataframe. It also contains the following functionality:
-Count number of table records
-Return information on a single customer.
-Return information on multiple customers
-Return a summary of customers with a credit limit >= user input
-List of table coulmns
-Deletion of a single record
-Deletion of all records.
"""

import gc
import sqlite3 as db
from pathlib import Path
import sys
import pandas as pd

DB_NAME = 'customers.db'
TABLE_NAME = 'customer'

DATA_SRC_PATH = Path.cwd().with_name('data') / 'customer.csv'

"""
Dictionary of for changing column/field names."""
COLUMN_NAMES = {'Id': 'customer_id',
                'Name': 'name',
                'Last_name': 'lastname',
                'Home_address': 'home_address',
                'Phone_number': 'phone_number',
                'Email_address': 'email',
                'Status': 'status',
                'Credit_limit': 'credit_limit'}


def connect():
    """
    Connects to salite database
    :return: open database
    """
    database = db.connect(DB_NAME)
    return database


def add_customer():
    """
    Function to read in csv and create new database and customer table.
    Table is not created if already extant.
    :return: database object containing a customer table
    """

    # read in the data
    data_in = pd.read_csv(DATA_SRC_PATH, encoding='ISO-8859-1') \
        .rename(columns=COLUMN_NAMES)
    # create new table
    data_in.to_sql(TABLE_NAME, con=connect(), if_exists='replace',
                   index=True, index_label='Unique_ID', chunksize=1000)
    # garbage collection
    gc.collect()


def total_records():
    """
    Retuns total number of records after adding records from source file.
    :return: Text of record count.
    """
    cursor = connect().cursor()
    cursor.execute(f'SELECT COUNT (*) FROM {TABLE_NAME}')
    count = cursor.fetchall()
    return f'Database has {count[0][0]:,.0f} total records.'


def search_customers(cust_id):
    """
    returns information about a specific customer
    :param cust_id:
    :return: name, lastname, email, phone number
    """
    search = connect().cursor()
    search.execute(f"SELECT customer_id, name, lastname, email,"
                   f" credit_limit FROM {TABLE_NAME}"
                   f" WHERE customer_id = '{cust_id}'")
    for row in search.fetchall():
        return f'{row[0]} {row[1]} {row[2]} {row[3]}'


def print_customer_search(customers):
    """
    Accepts a single customer id or a container of multiple and passes it/them
    to the search_customer function and prints the results
    :param customer_list:
    :return: console display of customer information
    """
    if isinstance(customers, str):
        print(search_customers(customers))
    else:
        for customer in customers:
            print(search_customers(customer))


def get_table_columns():
    """
    returns list of all table columns
    :return: list of column names
    """
    connection = connect().cursor()
    connection.execute(f'PRAGMA TABLE_INFO({TABLE_NAME})')
    column_names = [tup[1] for tup in connection.fetchall()]
    return column_names


def customer_limit_summary(credit_lim):
    """
    returns count and average credit limit of customers with a credit
    limit >= the passed argument
    entered amount
    :param credit_lim:
    :return: customer list based on credit limit
    """
    cursor = connect().cursor()
    container = [item[0] for item in cursor.execute(f"SELECT credit_limit"
                                                    f" FROM {TABLE_NAME} WHERE "
                                                    f"credit_limit >='"
                                                    f"{credit_lim}'")]
    return f'{len(container):,.0f} customers have a credit limit >=' \
        f' {credit_lim:,.0f} with and average limit of' \
        f' {sum(container) / len(container):,.0f}'


def del_single_customer(cust_id):
    """
    Deletes a customer specified by customer id
    :param cust_id:
    :return: record is deleted
    """
    conn = db.connect('customers.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customer "
                       "WHERE customer_id = '%s'" % cust_id)
        conn.commit()
    except RuntimeError as error:
        print(error)


def del_all_customers():
    """
    Deletes all customers in table. Returns total_records function
    as proof of deletion.
    :param cust_id:
    :return: record is deleted
    """
    conn = db.connect('customers.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer")
    conn.commit()
    return total_records()


def quit_the_program():
    """
    Simply quits the program.
    :return: closes the program
    """
    print('Tschüss')
    sys.exit()


if __name__ == '__main__':
    add_customer()


    def run_options():
        """
        Function for manual testing.
        :return: Function entered
        """
        answer = input("\n".join(("What database work would you like to do?",
                                  "Please select and option below:",
                                  "1 - Search for a single customer.",
                                  "2 - Search for a multiple customers.",
                                  "3 - Get a summary of customers based on "
                                  "redit limit.",
                                  "4 - Delete a customer record",
                                  "5 - Delete all customer records",
                                  "6 - View all column names",
                                  "7 - Quit",
                                  ">>> ", '\n')))
        if answer == '1':
            print_customer_search('C000002')
        elif answer == '2':
            print_customer_search(['C000002', 'C000003'])
        elif answer == '3':
            print(customer_limit_summary(900))
        elif answer == '4':
            del_single_customer("C000001")
        elif answer == '5':
            print(del_all_customers())
        elif answer == '6':
            print(get_table_columns())
        else:
            quit_the_program()


    while True:
        run_options()
