import basic_operations
import os
import unittest

TEST_DATABASE_FILENAME = 'testing.db'


class TestCustomer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """"
        Create database connection.
        """
        basic_operations.initialize_database(TEST_DATABASE_FILENAME)

    @classmethod
    def tearDownClass(cls):
        """
        Delete database file after all TestCustomer tests are finished.
        """
        try:
            os.remove(TEST_DATABASE_FILENAME)
        except FileNotFoundError:
            pass

    def setUp(self):
        """
        Populate database as a fixture prior to each TestCustomer test.
        """
        basic_operations.Customer.drop_table()
        basic_operations.Customer.create_table()
        customers = [('C000001', 'Shea', 'Boehm', '3343 Sallie Gateway', '508.363.0253 x4976',
                      'Alexander.Weber@monroe.com', 'Inactive',
                      461),
                     ('C000002', 'Abe', 'Anderson', '2324 Jefferson Dr.', '804.747.1181',
                      'antipathize@zgu5la23tngr2molii.cf', 'Active',
                      200),
                     ('C000003', 'Ben', 'Baker', '55 Opal Ave', '584.287.5797',
                      'reziac@yahoo.ca', 'Active',
                      343),
                     ('C000004', 'Cary', 'Crews', '78 Davis Dr', '689.270.5294',
                      'esokullu@mac.com', 'Inactive',
                      400),
                     ('C000005', 'Dan', 'Daniels', '3443 Brick Way', '515.526.1882',
                      'loscar@gmail.com', 'Active',
                      303),
                     ('C000006', 'Ed', 'Egerhdal', '11 Wood Trail', '788.465.7515',
                      'roesch@att.net', 'Inactive',
                      549),
                     ('C000007', 'Fred', 'Franks', '98 Lake Ave', '719.660.5746',
                      'tbusch@live.com', 'Active',
                      600),
                     ('C000008', 'Guy', 'Gundersen', '575 Sun Park Dr', '258.687.2964',
                      'skythe@live.com', 'Inactive',
                      280),
                     ]
        for (customer_id, first_name, last_name, home_address, phone_number, email_address, status, credit_limit)\
                in customers:
            db_record = basic_operations.Customer.create(customer_id=customer_id, first_name=first_name,
                                                         last_name=last_name, home_address=home_address,
                                                         phone_number=phone_number, email_address=email_address,
                                                         status=status, credit_limit=credit_limit)
            db_record.save()

    def tearDown(self):
        pass

    def test_add_customer(self):
        num_before = len(basic_operations.list_active_customers())
        basic_operations.add_customer('C000055', 'John', 'Doe', '100 Campus Dr', '555.343.1009', 'johndoe@myemail.com',
                                      'Active', 535)
        num_after = len(basic_operations.list_active_customers())
        self.assertEqual(num_after-num_before, 1)

    def test_delete_customer(self):
        delete_customer = 'C000005'
        basic_operations.delete_customer('C000005')
        self.assertEqual(delete_customer, 'C000005')

    def test_search_customer(self):
        search_customer = 'C000001'
        basic_operations.search_customer('C000001')
        self.assertEqual(search_customer, 'C000001')


if __name__ == '__main__':
    unittest.main()
