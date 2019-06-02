import datetime
import peewee
import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


DATABASE_NAME = 'customer.db'
DATABASE_CSV_FILE = '../data/customer.csv'

db = peewee.SqliteDatabase(DATABASE_NAME)


class Customer(peewee.Model):

    customer_id = peewee.CharField(primary_key=True, max_length=8)
    first_name = peewee.CharField(max_length=30)
    last_name = peewee.CharField(max_length=30)
    home_address = peewee.CharField(max_length=30)
    phone_number = peewee.CharField(max_length=30)
    email_address = peewee.CharField(max_length=30)
    status = peewee.CharField(max_length=8)
    credit_limit = peewee.IntegerField()

    class Meta:
        database = db
        db_table = 'customer'


def initialize_database(database_filename):
    db.init(database_filename)
    db.connect()


def add_tables():
    Customer.create_table()


def populate_database():
    db.execute_sql("PRAGMA foreign_keys = ON;")
    add_tables()
    print("Populating... %s" % datetime.datetime.now().strftime("%H:%M:%S"))
    with open(DATABASE_CSV_FILE, 'r', encoding='iso-8859-1') as f:
        for line in f.readlines()[1:]:
            record = line.rstrip('\n').split(',')
            if len(record) == 8:
                db_record = Customer.create(customer_id=record[0], first_name=record[1], last_name=record[2],
                                            home_address=record[3], phone_number=record[4], email_address=record[5],
                                            status=record[6], credit_limit=record[7])
                db_record.save()
    print("Finished. %s" % datetime.datetime.now().strftime("%H:%M:%S"))


def add_customer(customer_id,
                 first_name,
                 last_name,
                 home_address,
                 phone_number,
                 email_address,
                 status,
                 credit_limit):
    db_record = Customer.create(customer_id=customer_id, first_name=first_name, last_name=last_name,
                                home_address=home_address, phone_number=phone_number, email_address=email_address,
                                status=status, credit_limit=credit_limit)
    db_record.save()


def search_customer(customer_id):
    records = Customer.select().where(Customer.customer_id == customer_id)
    for rec in records:
        return "%s %s" % (rec.first_name, rec.last_name)


def list_active_customers():
    count = 0
    try:
        LOGGER.info('Counting active customers')
        query = (Customer.select(Customer.customer_id, Customer.status)
                 .where(Customer.status == 'active'))
        count = query.select().count()
    except Exception as error:
        LOGGER.info('Customer does not exist')

    return count


def delete_customer(customer_id):
    LOGGER.info('Deleting a customer')
    try:
        customer_delete = Customer.get(Customer.customer_id == customer_id)
        customer_delete.delete_instance()
        LOGGER.info(f'Customer with ID {customer_id} deleted')

    except Exception as error:
        LOGGER.info(f'Customer with ID {customer_id} not deleted')


def update_customer_credit(customer_id, new_credit_limit):
    query = Customer.update(credit_limit=new_credit_limit).where(Customer.customer_id == customer_id)
    n = query.execute()
    if not query.execute():
        raise ValueError("NoCustomer")


def main():
    if not os.path.isfile(DATABASE_NAME):
        initialize_database(DATABASE_NAME)
        populate_database()
    else:
        initialize_database(DATABASE_NAME)

    print(search_customer('C000004'))
    print(search_customer('C000016'))

    active_customers = list_active_customers()
    print('First 10 of %s active customers:' % len(active_customers))
    for (i, customer) in enumerate(active_customers):
        print('%s: %s' % (i, customer))
        if i == 10:
            break
    print('')

    print('Deleted %s customers.' % delete_customer('C000002'))
    print('Deleted %s customers.' % delete_customer('C000015'))
    print('')

    print('Changed credit score of customer C000003')
    print('')
    update_customer_credit('C000003', 981)


if __name__ == "__main__":
    main()
