# basic_operations.py
import datetime
import peewee
import os

DATABASE_NAME = 'customer.db'
DATABASE_CSV_FILE = '../data/customer.csv'
# DATABASE_CSV_FILE = 'customer_small.csv'

# db = peewee.SqliteDatabase(DATABASE_NAME)
db = peewee.SqliteDatabase(None)


class Customer(peewee.Model):
    """Define customer in the customer database"""

    customer_id = peewee.CharField(primary_key=True, max_length=8)
    first_name = peewee.CharField(max_length=30)
    last_name = peewee.CharField(max_length=30)
    home_address = peewee.CharField(max_length=30)
    phone_number = peewee.CharField(max_length=30)
    email_address = peewee.CharField(max_length=30)
    status = peewee.CharField(max_length=8)
    credit_limit = peewee.IntegerField()
    
    class Meta:
        """Meta class"""

        database = db
        db_table = 'customer'


def initialize_database(database_filename):
    db.init(database_filename)
    db.connect()


def add_tables():
    """Add tables to database"""
    Customer.create_table()


def populate_database():
    """Populate database from CSV file"""

    db.execute_sql("PRAGMA foreign_keys = ON;")
    add_tables()

    print("Populating... %s" % datetime.datetime.now().strftime("%H:%M:%S"))
    with open(DATABASE_CSV_FILE, 'r', encoding='iso-8859-1') as f:
        for line in f.readlines()[1:]:
            record = line.rstrip('\n').split(',')
            if len(record) == 8:
                # C000008,Faye,Gusikowski,329 Maye Wall,201.358.6143,Lelia_Wunsch@maximo.biz,Active,222
                # C000009,Nikko,Homenick,5348 Harann Haven,1-291-283-6287 x42360,Hans@camren.tv,Active,254
                # record[0] # customer ID
                # record[1] # first name
                # record[2] # last name
                # record[3] # home address
                # record[4] # phone number
                # record[5] # email
                # record[6] # status
                # record[7] # credit limit

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
    """Add customer to the database"""
    db_record = Customer.create(customer_id=customer_id, first_name=first_name, last_name=last_name,
                                home_address=home_address, phone_number=phone_number, email_address=email_address,
                                status=status, credit_limit=credit_limit)
    db_record.save()


def search_customer(customer_id):
    """Search for customer in the database"""
    records = Customer.select().where(Customer.customer_id == customer_id)
    for rec in records:
        return "%s %s" % (rec.first_name, rec.last_name)


def list_active_customers():
    """Get all customers currently in the database"""
    records = Customer.select().where(Customer.status == 'Active')
    return ['%s %s %s   credit=%s' % (rec.customer_id, rec.first_name, rec.last_name, rec.credit_limit)
            for rec in records]


def delete_customer(customer_id):
    """Delete customer from the database"""
    return Customer.delete_by_id(customer_id)


def update_customer_credit(customer_id, new_credit_limit):
    """Change customer's credit limit"""
    query = Customer.update(credit_limit=new_credit_limit).where(Customer.customer_id == customer_id)
    n = query.execute()

  
def main():
    """Run main sequence"""

    # if database file doesn't exist, connect (which creates one) and populate
    # else assume that the database is populated
    if not os.path.isfile(DATABASE_NAME):
        initialize_database(DATABASE_NAME)
        populate_database()
    else:
        initialize_database(DATABASE_NAME)

    print(search_customer('C000008'))
    print(search_customer('C000009'))

    active_customers = list_active_customers()
    print('First 10 of %s active customers:' % len(active_customers))
    for (i, customer) in enumerate(active_customers):
        print('%s: %s' % (i, customer))
        if i == 10:
            break
    print('')

    print('Deleted %s customers.' % delete_customer('C000009'))
    print('Deleted %s customers.' % delete_customer('C000013'))
    print('')

    print('Changed credit score of customer C000002')
    print('')
    update_customer_credit('C000002', 777)
   
    
    
if __name__ == "__main__":
    main()
