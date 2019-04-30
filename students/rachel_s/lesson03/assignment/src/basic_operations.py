#!/usr/bin/env python3

'''Creates functions for basic operations in the customer database'''

# Rachel Schirra
# April 13, 2019
# Python 220 Lesson 02

import csv
import model
from loguru import logger
from peewee import *


def connect_db(db_name):
    '''
    Connects to the specified database using peewee
    '''
    db = SqliteDatabase(db_name)
    return db.connect()


def add_customer(
        customer_id,
        name,
        lastname,
        home_address,
        phone_number,
        email_address,
        status,
        credit_limit
    ):
    '''
    Adds a new customer to the database with the following info:
    customer_id: Customer ID (numeric)
    name: Given name (char)
    lastname: Surname (char)
    home_address: Home address (char)
    phone_number: Phone number. May include extension. (char)
    email_address: Email address. Contains one @ and at least one . (char)
    status: Customer status (char)
    credit_limit: Credit limit (numeric)
    '''
    connect_db('customer.db')
    try:
        temp_customer = model.Customer.create(
            Customer_id=customer_id,
            Name=name,
            Lastname=lastname,
            Home_address=home_address,
            Phone_number=phone_number,
            Email_address=email_address,
            Status=status,
            Credit_limit=int(credit_limit)
        )
        temp_customer.save()
        return True
    except IntegrityError as err:
        logger.warning(err)
        return False


def load_data(filename):
    '''
    Imports customer data from CSV file.
    Returns a list of customer dictionaries that can be shoved into the
    db.
    Fails loudly if something goes wrong.
    '''
    cust_dicts = []
    logger.debug('Attempting to read file {}.'.format(filename))
    with open(filename, 'r') as file:
        try:
            csv_reader = csv.DictReader(file, delimiter=',', )
            logger.debug('Successfully loaded file {}'.format(filename))
            for row in csv_reader:
                cust_dicts.append(dict(row))
        except(FileNotFoundError, ValueError) as err:
            logger.error(err)
    return cust_dicts


def customer_db_import(cust_dicts):
    '''
    Transfers customer data from a list of dictionaries into the db.
    Takes a list of dicts. Assumes they are the right shape.
    Doesn't return anything, just shoves all those customers into the db.
    Doesn't do anything fancy like check for duplicates.
    '''
    for cust in cust_dicts:
        logger.debug('Adding customer {} to DB.'.format(cust['Id']))
        add_customer(
            cust['Id'],
            cust['Name'],
            cust['Last_name'],
            cust['Home_address'],
            cust['Phone_number'],
            cust['Email_address'],
            cust['Status'].lower(),
            int(cust['Credit_limit'])
        )


def search_customer(customer_id):
    '''
    Searches for customer by alphanumeric ID. Returns customer dictionary.
    If no such customer is found, returns empty dictionary.
    '''
    connect_db('customer.db')
    logger.debug('Finding record for {}'.format(customer_id))
    try:
        cust = model.Customer.get(model.Customer.Customer_id == customer_id)
    except Exception:
        logger.debug('Record {} not found, returning empty '
                     'dict.'.format(customer_id))
        return {}
    cust_dict = {
        'name': cust.Name,
        'lastname': cust.Lastname,
        'email': cust.Email_address,
        'phone_number': cust.Phone_number
    }
    return cust_dict


def delete_customer(customer_id):
    '''
    Deletes the customer with the given ID from the database.
    Returns True if the customer was successfully deleted, and
    False if not.
    '''
    cust = get_customer(customer_id)
    try:
        cust.delete_instance()
        cust.save()
    except Exception as err:
        logger.error(err)
        return False
    return True


def update_customer_credit(customer_id, credit_limit):
    '''
    Alters the given customer's numeric credit limit
    '''
    # cust = get_customer(customer_id)
    try:
        cust = model.Customer.get(model.Customer.Customer_id == customer_id)
    except IndexError:
        logger.warning('Customer {} not found'.format(customer_id))
    try:
        cust.Credit_limit = int(credit_limit)
        cust.save()
    except Exception as err:
        logger.warning(err)


def list_active_customers():
    '''
    Returns the number of customers with status Active as an integer
    '''
    logger.debug('Counting customers with acrive status.')
    count = model.Customer.select().where(
        model.Customer.Status == 'active').count()
    return count


def get_customer(customer_id):
    '''
    Returns the Customer object of a customer with a given ID.
    Throws an error if the customer is not found. Do not use if you
    want it to do something else if the customer doesn't exist.
    '''
    try:
        cust = model.Customer.get(model.Customer.Customer_id == customer_id)
        return cust
    except(IndexError):
        logger.error('Record {} not found.'.format(customer_id))
        raise(IndexError)

