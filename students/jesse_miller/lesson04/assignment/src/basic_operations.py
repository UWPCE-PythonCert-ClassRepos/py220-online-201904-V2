#!/usr/bin/env python3
'''
Creating customer database for Norton Furniture
'''
import sqlite3
import logging
import csv
import peewee
import customer_schema as cs
import customer_creation as cc

# pylint: disable=C0103
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

log_file = logging.FileHandler('db.log')
log_file.setLevel(logging.DEBUG)

log_format = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d\
%(levelname)s %(message)s')

log_file.setFormatter(log_format)

logger.addHandler(log_file)
log_stream = logging.StreamHandler()
log_stream.setLevel(logging.DEBUG)
log_stream.setFormatter(log_format)

logging.info('Starting basic operations for customer database.')

# pylint: disable=R0913
def add_customer(customer_id, first_name, last_name, home_address, phone_number,
                 email_address, active_status, credit_limit):
    '''
    Adding a new customer to the DB
    '''
    try:
        new_customer = cs.Customer.create(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            phone_number=phone_number,
            email_address=email_address,
            active_status=active_status,
            credit_limit=credit_limit)
        new_customer.save()
        logging.info('%s %s has been added to the database.', first_name,
                     last_name)
    except peewee.IntegrityError as add_error:
        logging.error('%s. Error cannot add %s %s to the database.', add_error,
                      first_name, last_name)
        raise peewee.IntegrityError


def delete_customer(customer_id):
    '''
    Deleting a customer from the DB
    '''
    try:
        former_customer = cs.Customer.get(cs.Customer.customer_id == customer_id)
        logging.info('%s: %s %s has been removed from the database.', customer_id,
                     former_customer.first_name, former_customer.last_name)
        former_customer.delete_instance()
    except peewee.DoesNotExist:
        logging.error('Non-existant customer.')


def search_customer(customer_id):
    '''
    Search DB for an active customer
    '''
    try:
        current_customer = cs.Customer.get(cs.Customer.customer_id == customer_id)

        customer_dict = {'first_name': current_customer.first_name,
                         'last_name': current_customer.last_name,
                         'email_address': current_customer.email_address,
                         'phone_number': current_customer.phone_number}
        logging.info('%s: %s %s exists', customer_id,
                     current_customer.first_name, current_customer.last_name)

        return customer_dict

    except peewee.DoesNotExist:
        logging.error('Non-existant customer.')
        return dict()


def list_active_customers():
    '''
    List all active customers
    '''
    total_custs = (cs.Customer.select().where(cs.Customer.active_status).count())

    logging.info('The current number of active customers is %s', total_custs)

    return total_custs


def update_customer_credit(customer_id, new_limit):
    '''
    Update customer credit limits
    '''
    try:
        update_cust = cs.Customer.get(cs.Customer.customer_id == customer_id)
        update_cust.credit_limit = new_limit
        update_cust.save()
        logging.info('Raise credit limit for %s %s to %s',
                     update_cust.first_name, update_cust.last_name, new_limit)

    except peewee.DoesNotExist:
        logging.error('Unable to comply, customer does not exist')
        raise peewee.DoesNotExist


def import_cust_file():
    '''
    Importing the customer csv.  Had to add a way to skip the header to keep
    everything in the DB sane and uniform.  This currently does not work,
    although I feel it should.
    '''
    # pylint: disable=C0103
    filename = 'customer.csv'
    with open(filename, 'r', encoding="ISO-8859-1") as f:
        next(f, None)  # skip the header row
        reader = csv.reader(f)

        sql = sqlite3.connect('customers.db')
        logging.info('Opening database')
        cursor = sql.cursor()

        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS Customer
                        (customer_id,
                        first_name,
                        last_name,
                        home_address,
                        phone_number,
                        email_address,
                        status,
                        credit_limit)''')

            for row in reader:
                cursor.execute('INSERT INTO customer VALUES ?, ?, ?, ?, ?, ?, \
                               ?, ?)', row)
            logging.info('Import successful')
            sql.commit()
            logging.info('Import committed')
            sql.close()
        # pylint: disable=W0703
        except Exception as error:
            logging.error('Unable to load customer data')
            logging.error(error)

        logging.info('Import transaction complete')


def output_cust():
    '''
    Prints the customer information from the DB (Okay, I see what the problem is
    here.  I just have to figure out how to do what I need.  Or at least I think
    I do.  I think that, there's not a database currently to test at this point.
    But I may also be misinterpreting what's happening by this stage.)
    '''
    all_records = cs.Customer.select()

    for person in all_records:
        print(f'Customer ID: {person.customer_id}\nFirst Name: \
        {person.first_name}\nLast Name: {person.last_name}\n'
              f'Home Address: {person.home_address}\nPhone Number: \
        {person.phone_number}\n' f'Email Address: {person.email_address}\n\
        Status: {person.status}\nCredit Limit: ${person.credit_limit}\n')


if __name__ == 'main':
    cc.main()
    import_cust_file()
    output_cust()
