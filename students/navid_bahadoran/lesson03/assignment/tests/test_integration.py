import pytest
from peewee import IntegrityError
import src.basic_operations as l


@pytest.fixture
def _customer():
    return [
        ('C000000', 'Rickey', 'Shanahan', '337 Eichmann Locks', '1-615-598-8649 x975', 'Jessy@myra.net', 'Active', 237),
        ('C000001', 'Shea', 'Boehm', '3343 Sallie Gateway', '508.104.0644 x4976', 'Alexander.Weber@monroe.com',
         'Inactive', 461),
        (
            'C000002', 'Blanca', 'Bashirian', '0193 Malvina Lake', '(240)014-9496 x08349', 'Joana_Nienow@guy.org',
            'Active',
            689),
        (
            'C000003', 'Elfrieda', 'Skiles', '3180 Mose Row', '(839)825-0058', 'Mylene_Smitham@hannah.co.uk', 'Active',
            90),
        ('C000004', 'Mittie', 'Turner', '996 Lorenza Points', '1-324-023-8861 x025', 'Clair_Bergstrom@rylan.io',
         'Active', 565),
        ('C000005', 'Nicole', 'Wisozk', '0170 Kuphal Knoll', '(731)775-3683 x45318', 'Hudson.Witting@mia.us', 'Active',
         244),
        ('C000006', 'Danika', 'Bechtelar', '5067 Goyette Place', '503-011-7566 x19729', 'Wyatt.Hodkiewicz@wyatt.net',
         'Active', 663),
        ('C000007', 'Elbert', 'Abbott', '36531 Bergstrom Circle', '(223)402-1096', 'Isabelle_Rogahn@isac.biz', 'Active',
         480),
        ('C000008', 'Faye', 'Gusikowski', '329 Maye Wall', '201.358.6143', 'Lelia_Wunsch@maximo.biz', 'Active', 222),
        (
            'C000009', 'Nikko', 'Homenick', '5348 Harªann Haven', '1-291-283-6287 x42360', 'Hans@camren.tv', 'Active',
            254),
        ('C000010', 'Ruthe', 'Batz', '186 Theodora Parkway', '1-642-296-4711 x359', 'Oren@sheridan.name', 'Inactive',
         508)]


def test_integration_basic_operation(_customer):
    for customer in _customer:
        l.add_customer(*customer)
    for customer in _customer:
        assert l.search_customer(customer[0])['name'] == customer[1]
        assert l.search_customer(customer[0])['last_name'] == customer[2]
    with pytest.raises(IntegrityError) as e:
        l.add_customer(*_customer[0])
        assert "DoubleEntry" in str(e.value)
    l.update_customer_credit("C000000", 10000)
    assert l.search_customer('C000000')['credit_limit'] == 10000
    with pytest.raises(ValueError) as e:
        l.update_customer_credit("C001011", 10)
        assert 'NoCustomer' in str(e.value)
    assert l.list_active_customers() == 9

    for customer in _customer:
        assert l.delete_customer(customer[0]) is True
        assert l.search_customer(customer[0]) == {}
