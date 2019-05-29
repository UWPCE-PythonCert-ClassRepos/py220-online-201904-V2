"""grade lesson 5
"""

import pytest
import src.database_operations as l


@pytest.fixture
def _show_available_products():
    """ Expected output for show available products call """
    return {
        "P000001": {
            "description": "Chair Red leather",
            "product_type": "Livingroom",
            "quantity_available": "21",
        },
        "P000002": {
            "description": "Table Oak",
            "product_type": "Livingroom",
            "quantity_available": "4",
        },
        "P000003": {
            "description": "Couch Green cloth",
            "product_type": "Livingroom",
            "quantity_available": "10",
        },
        "P000004": {
            "description": "Dining table Plastic",
            "product_type": "Kitchen",
            "quantity_available": "23",
        },
        "P000005": {
            "description": "Stool Black ash",
            "product_type": "Kitchen",
            "quantity_available": "12",
        },
        "P000006": {
            "description": "Chair Red leather",
            "product_type": "Livingroom",
            "quantity_available": "21",
        },
        "P000007": {
            "description": "Table Oak",
            "product_type": "Livingroom",
            "quantity_available": "4",
        },
        "P000008": {
            "description": "Couch Green cloth",
            "product_type": "Livingroom",
            "quantity_available": "10",
        },
        "P000009": {
            "description": "Dining table Plastic",
            "product_type": "Kitchen",
            "quantity_available": "23",
        },
    }


@pytest.fixture
def _list_all_customers():
    """ Expected output for list all customeers """
    return {
        "C000000": {
            "Credit_limit": "237",
            "Email_address": "Jessy@myra.net",
            "Home_address": "337 Eichmann Locks",
            "Last_name": "Shanahan",
            "Name": "Rickey",
            "Phone_number": "1-615-598-8649 x975",
            "Status": "Active",
        },
        "C000001": {
            "Credit_limit": "461",
            "Email_address": "Alexander.Weber@monroe.com",
            "Home_address": "3343 Sallie Gateway",
            "Last_name": "Boehm",
            "Name": "Shea",
            "Phone_number": "508.104.0644 x4976",
            "Status": "Inactive",
        },
        "C000002": {
            "Credit_limit": "689",
            "Email_address": "Joana_Nienow@guy.org",
            "Home_address": "0193 Malvina Lake",
            "Last_name": "Bashirian",
            "Name": "Blanca",
            "Phone_number": "(240)014-9496 x08349",
            "Status": "Active",
        },
        "C000003": {
            "Credit_limit": "90",
            "Email_address": "Mylene_Smitham@hannah.co.uk",
            "Home_address": "3180 Mose Row",
            "Last_name": "Skiles",
            "Name": "Elfrieda",
            "Phone_number": "(839)825-0058",
            "Status": "Active",
        },
        "C000004": {
            "Credit_limit": "565",
            "Email_address": "Clair_Bergstrom@rylan.io",
            "Home_address": "996 Lorenza Points",
            "Last_name": "Turner",
            "Name": "Mittie",
            "Phone_number": "1-324-023-8861 x025",
            "Status": "Active",
        },
        "C000005": {
            "Credit_limit": "244",
            "Email_address": "Hudson.Witting@mia.us",
            "Home_address": "0170 Kuphal Knoll",
            "Last_name": "Wisozk",
            "Name": "Nicole",
            "Phone_number": "(731)775-3683 x45318",
            "Status": "Active",
        },
        "C000006": {
            "Credit_limit": "663",
            "Email_address": "Wyatt.Hodkiewicz@wyatt.net",
            "Home_address": "5067 Goyette Place",
            "Last_name": "Bechtelar",
            "Name": "Danika",
            "Phone_number": "503-011-7566 x19729",
            "Status": "Active",
        },
        "C000007": {
            "Credit_limit": "480",
            "Email_address": "Isabelle_Rogahn@isac.biz",
            "Home_address": "36531 Bergstrom Circle",
            "Last_name": "Abbott",
            "Name": "Elbert",
            "Phone_number": "(223)402-1096",
            "Status": "Active",
        },
        "C000008": {
            "Credit_limit": "222",
            "Email_address": "Lelia_Wunsch@maximo.biz",
            "Home_address": "329 Maye Wall",
            "Last_name": "Gusikowski",
            "Name": "Faye",
            "Phone_number": "201.358.6143",
            "Status": "Active",
        },
    }


@pytest.fixture
def _list_all_products():
    """ Expected output for list_all_products() """
    return {
        "P000001": {
            "description": "Chair Red leather",
            "product_type": "Livingroom",
            "quantity_available": "21",
        },
        "P000002": {
            "description": "Table Oak",
            "product_type": "Livingroom",
            "quantity_available": "4",
        },
        "P000003": {
            "description": "Couch Green cloth",
            "product_type": "Livingroom",
            "quantity_available": "10",
        },
        "P000004": {
            "description": "Dining table Plastic",
            "product_type": "Kitchen",
            "quantity_available": "23",
        },
        "P000005": {
            "description": "Stool Black ash",
            "product_type": "Kitchen",
            "quantity_available": "12",
        },
        "P000006": {
            "description": "Chair Red leather",
            "product_type": "Livingroom",
            "quantity_available": "21",
        },
        "P000007": {
            "description": "Table Oak",
            "product_type": "Livingroom",
            "quantity_available": "4",
        },
        "P000008": {
            "description": "Couch Green cloth",
            "product_type": "Livingroom",
            "quantity_available": "10",
        },
        "P000009": {
            "description": "Dining table Plastic",
            "product_type": "Kitchen",
            "quantity_available": "23",
        },
    }


@pytest.fixture
def _list_rentals_for_customer():
    """ Expected output for list_rentals_for_customers """
    return [
        {
            "description": "Couch Green cloth",
            "product_id": "P000003",
            "product_type": "Livingroom",
        },
        {
            "description": "Dining table Plastic",
            "product_id": "P000004",
            "product_type": "Kitchen",
        },
    ]


@pytest.fixture
def _list_customers_renting_product():
    """ Expected output for list_rentals_for_customers """
    return [
        {
            "Credit_limit": "237",
            "Email_address": "Jessy@myra.net",
            "Home_address": "337 Eichmann Locks",
            "Last_name": "Shanahan",
            "Name": "Rickey",
            "Phone_number": "1-615-598-8649 x975",
            "Status": "Active",
            "user_id": "C000000",
        },
        {
            "Credit_limit": "244",
            "Email_address": "Hudson.Witting@mia.us",
            "Home_address": "0170 Kuphal Knoll",
            "Last_name": "Wisozk",
            "Name": "Nicole",
            "Phone_number": "(731)775-3683 x45318",
            "Status": "Active",
            "user_id": "C000005",
        },
        {
            "Credit_limit": "222",
            "Email_address": "Lelia_Wunsch@maximo.biz",
            "Home_address": "329 Maye Wall",
            "Last_name": "Gusikowski",
            "Name": "Faye",
            "Phone_number": "201.358.6143",
            "Status": "Active",
            "user_id": "C000008",
        },
    ]


@pytest.fixture
def _list_all_rentals():
    """ Expected output for list_all_rentals """
    return {
        "C000000": {
            "address": "337 Eichmann Locks",
            "email": "Jessy@myra.net",
            "name": "Rickey Shanahan",
            "phone_number": "1-615-598-8649 x975",
            "product_id": "P000001",
        },
        "C000001": {
            "address": "3343 Sallie Gateway",
            "email": "Alexander.Weber@monroe.com",
            "name": "Shea Boehm",
            "phone_number": "508.104.0644 x4976",
            "product_id": "P000004",
        },
        "C000003": {
            "address": "3180 Mose Row",
            "email": "Mylene_Smitham@hannah.co.uk",
            "name": "Elfrieda Skiles",
            "phone_number": "(839)825-0058",
            "product_id": "P000003",
        },
        "C000004": {
            "address": "996 Lorenza Points",
            "email": "Clair_Bergstrom@rylan.io",
            "name": "Mittie Turner",
            "phone_number": "1-324-023-8861 x025",
            "product_id": "P000004",
        },
        "C000005": {
            "address": "0170 Kuphal Knoll",
            "email": "Hudson.Witting@mia.us",
            "name": "Nicole Wisozk",
            "phone_number": "(731)775-3683 x45318",
            "product_id": "P000001",
        },
        "C000008": {
            "address": "329 Maye Wall",
            "email": "Lelia_Wunsch@maximo.biz",
            "name": "Faye Gusikowski",
            "phone_number": "201.358.6143",
            "product_id": "P000001",
        },
        "C000009": {
            "address": "5348 Harªann Haven",
            "email": "Hans@camren.tv",
            "name": "Nikko Homenick",
            "phone_number": "1-291-283-6287 x42360",
            "product_id": "P000002",
        },
        "C000010": {
            "address": "186 Theodora Parkway",
            "email": "Oren@sheridan.name",
            "name": "Ruthe Batz",
            "phone_number": "1-642-296-4711 x359",
            "product_id": "P000005",
        },
    }


@pytest.fixture
def _linear_insert():
    """ Pytest fixture for linear insert """
    return [
        {"customers": {"fail": 0, "success": 9, "total_records": 9}},
        {"product": {"fail": 0, "success": 9, "total_records": 9}},
        {"rental": {"fail": 0, "success": 9, "total_records": 9}},
    ]


@pytest.fixture
def _parallel_insert():
    """ Pytest fixture for parallel insert """
    return [
        {"customers": {"fail": 0, "success": 9, "total_records": 9}},
        {"product": {"fail": 0, "success": 9, "total_records": 9}},
        {"rental": {"fail": 0, "success": 9, "total_records": 9}},
    ]


def test_linear(_linear_insert):
    """ parallel import csv """
    l.drop_database()
    results = l.linear(
        ["./data/customers.csv", "./data/product.csv", "./data/rental.csv"]
    )

    for result in results:
        del result[next(iter(result))]["elapsed"]

    assert _linear_insert == results


def test_parallel(_linear_insert):
    """ parallel import csv """
    l.drop_database()
    results = l.parallel(
        ["./data/customers.csv", "./data/product.csv", "./data/rental.csv"]
    )

    for result in results:
        del result[next(iter(result))]["elapsed"]

    assert _linear_insert == results


def test_insert_to_mongo():
    """ import given csv file into mongo """

    # l.drop_database()
    l.drop_collections()

    results = l.insert_to_mongo("./data/product.csv")
    results = results["product"]
    assert results["success"] == 9
    assert results["fail"] == 0
    assert results["total_records"] == 9
    assert results["elapsed"] > 0

    results = l.insert_to_mongo("./data/customers.csv")
    results = results["customers"]
    assert results["success"] == 9
    assert results["fail"] == 0
    assert results["total_records"] == 9
    assert results["elapsed"] > 0

    results = l.insert_to_mongo("./data/rental.csv")
    results = results["rental"]
    assert results["success"] == 9
    assert results["fail"] == 0
    assert results["total_records"] == 9
    assert results["elapsed"] > 0

    results = l.insert_to_mongo("./data/product.csv")
    results = results["product"]
    assert results["success"] == 0
    assert results["fail"] == 9
    assert results["total_records"] == 9
    assert results["elapsed"] > 0

    results = l.insert_to_mongo("./data/customers.csv")
    results = results["customers"]
    assert results["success"] == 0
    assert results["fail"] == 9
    assert results["total_records"] == 9
    assert results["elapsed"] > 0

    results = l.insert_to_mongo("./data/rental.csv")
    results = results["rental"]
    assert results["success"] == 0
    assert results["fail"] == 9
    assert results["total_records"] == 9
    assert results["elapsed"] > 0


def test_show_available_products(_show_available_products):
    """ available products """
    l.drop_database()
    l.insert_to_mongo("./data/product.csv")
    l.DB_NAME = "HPNorton_PyMongo_L07"
    students_response = l.show_available_products()
    assert students_response == _show_available_products


def test_show_rentals(_list_customers_renting_product):
    """ rentals """
    l.drop_database()
    l.insert_to_mongo("./data/customers.csv")
    l.insert_to_mongo("./data/product.csv")
    l.insert_to_mongo("./data/rental.csv")
    students_response = l.customers_renting_product("P000001")
    assert students_response == _list_customers_renting_product


def test_list_all_customers(_list_all_customers):
    """ customers """
    l.drop_database()
    l.insert_to_mongo("./data/customers.csv")
    my_response = l.list_all_customers()
    assert my_response == _list_all_customers


def test_list_all_products(_list_all_products):
    """ customers """
    l.drop_database()
    l.insert_to_mongo("./data/product.csv")
    my_response = l.list_all_products()
    assert my_response == _list_all_products


def test_list_all_rentals(_list_all_rentals):
    """ customers """
    l.drop_database()
    l.insert_to_mongo("./data/rental.csv")
    my_response = l.list_all_rentals()
    assert my_response == _list_all_rentals


def test_rentals_for_customer(_list_rentals_for_customer):
    """ rentals for customers """
    l.drop_database()
    l.insert_to_mongo("./data/customers.csv")
    l.insert_to_mongo("./data/product.csv")
    l.insert_to_mongo("./data/rental.csv")
    my_response = l.rentals_for_customer("C000001")
    assert my_response == _list_rentals_for_customer


def test_get_line():
    """ Test get_line function """
    lines = [x for x in range(10)]
    for num, line in enumerate(l.get_line(lines)):
        assert line == lines[num]


def test_open_file():
    """ Test open file function """
    file = l.open_file("./data/customers.csv")

    with open("./data/customers.csv", "rb") as content:
        next(content)
        lines = content.read().decode("utf-8-sig", errors="ignore").split("\n")
        for line in lines:
            assert line in file


def test_drop_databases():
    """ Test drop HPNorton database """

    l.insert_to_mongo("./data/customers.csv")
    assert "HPNorton_PyMongo_L09" in l.MONGO.connection.list_database_names()
    l.drop_database()
    assert (
        "HPNorton_PyMongo_L09" not in l.MONGO.connection.list_database_names()
    )


def test_drop_collections():
    """ Test drop HPNorton collections """

    l.insert_to_mongo("./data/customers.csv")
    l.insert_to_mongo("./data/product.csv")
    l.insert_to_mongo("./data/rental.csv")
    collection_names = (
        l.MONGO.connection.HPNorton_PyMongo_L09.list_collection_names()
    )
    assert "customers" in collection_names
    assert "product" in collection_names
    assert "rental" in collection_names
    l.drop_collections()
    collection_names = (
        l.MONGO.connection.HPNorton_PyMongo_L09.list_collection_names()
    )
    assert "customers" not in collection_names
    assert "product" not in collection_names
    assert "rental" not in collection_names
