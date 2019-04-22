"""Unit test for basic operations program"""

# pylint: disable= C0303, C0305, E0401
import pytest
import customer_model as cm
import basic_operations as bo


# create a set of customers
@pytest.fixture
def _add_customers():    
    return[('1234', 'Jon', 'Malone', '446 Hamtramock ave', '0294975592',

            'jonmaloney@yahoo.com', True,

            2000.00),

           ('646', 'David', 'Moon',

            '788 Evergreen way', '014445555',

            'davidmoon@gmail.com', False,

            6000.00),

           ('9899', 'Paul', 'Allen',

            '5334 Madison ave', '096667777',

            'paulallen@gmail.com', True,

            99999.50),]


def drop_db():

    """Drops customer table"""
    cm.database.drop_tables([cm.Customer])
    cm.database.close()

def create_empty_db():

    """Creates an empty customer database"""
    drop_db()
    cm.database.create_tables([cm.Customer])
    cm.database.close()
    
def test_add_customer(_add_customers):
    """Tests if a new customer is added to database"""
    create_empty_db()
    for customer in _add_customers:
        bo.add_customer(*customer)
        added = bo.search_customer(customer[0])
        assert added["name"] == customer[1]
        assert added["lastname"] == customer[2]
        assert added["email"] == customer[5]
        assert added["phone_number"] == customer[4]


def test_search_customer(_add_customers):
    """Tests customer search function"""
    create_empty_db()
    for customer in _add_customers:
        bo.add_customer(*customer)
        result = bo.search_customer(_add_customers[0])
        assert result == {}        
        result = bo.search_customer(customer[0])
        assert result["name"] == customer[1]
        assert result["lastname"] == customer[2]
        assert result["email"] == customer[5]
        assert result["phone_number"] == customer[4]
        

def test_search_customer_not_found():
    """
    Tests search_customer returns an empty dictionary when customer not found
    """
    returned_customer = bo.search_customer('bad id')
    assert returned_customer == {}

def test_delete_customer(_add_customers):
    """Tests if user can delete customer """
    create_empty_db()
    for customer in _add_customers:
        bo.add_customer(customer[0],
                        customer[1],
                        customer[2],
                        customer[3],
                        customer[4],
                        customer[5],
                        customer[6],
                        customer[7]
                        )
       
        bo.delete_customer(customer[0])
        assert bo.search_customer(customer[0]) == {}


def test_list_active_customers(_add_customers):
    """Tests list of active customers"""
#    create_empty_db()
    for customer in _add_customers:
        bo.add_customer(customer[0],
                        customer[1],
                        customer[2],
                        customer[3],
                        customer[4],
                        customer[5],
                        customer[6],
                        customer[7]
                        )
    actives = bo.list_active_customers()
    assert actives == 2
    for customer in _add_customers:
        bo.delete_customer(customer[0])
    
        
def test_update_customer_credit(_add_customers):
    """Tests if customer credit is updated properly"""
    create_empty_db()
    for customer in _add_customers:
        bo.add_customer(customer[0],
                        customer[1],
                        customer[2],
                        customer[3],
                        customer[4],
                        customer[5],
                        customer[6],
                        customer[7]
                        )
        bo.update_customer_credit(customer[0], 5000.00)
        query = cm.Customer.get(cm.Customer.customer_id == customer[0])
        assert query.customer_limit == 5000.00
        with pytest.raises(ValueError):
            bo.update_customer_credit('456879', 5000.00)




