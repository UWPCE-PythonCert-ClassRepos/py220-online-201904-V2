# pylint: disable=E0401, W0401
"""
    Tests for create_db.py
"""


import logging
from peewee import *
import create_db as cdb


def test_add_tables():
    """Test add_tables function
    """
    cdb.add_tables()
    fields = str(cdb.db.database.get_columns("Customer"))
    assert "customer_id" in fields
    assert "name" in fields
    assert "last_name" in fields
    assert "home_address" in fields
    assert "phone_number" in fields
    assert "email_address" in fields
    assert "status" in fields
    assert "credit_limit" in fields


def test_get_line():
    """Test get_line function
    """
    lines = [x for x in range(10)]
    for num, line in enumerate(cdb.get_line(lines)):
        assert line == lines[num]


def test_open_file():
    """Test open file function
    """
    file = cdb.open_file("./data/head-cust.csv")

    with open("./data/head-cust.csv", "rb") as content:
        next(content)
        lines = content.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines:
            assert line in file


def test_parse_cmd_arguments():
    """Test parse_cmd_arguments function
    """
    parser = cdb.parse_cmd_arguments(["-i", "./data/head-cust.csv"])
    print(parser.input)
    assert parser.input == "./data/head-cust.csv"
    assert parser.blank is False
    parser = cdb.parse_cmd_arguments(["-i", "./data/head-cust.csv", "-b"])
    assert parser.blank is True


def test_populate_database():
    """Test populate_database function
    """
    # Seed database
    with open("./data/head-cust.csv", "rb") as content:
        next(content)
        lines = content.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines:
            cdb.populate_database(line)

    # Make sure we cover the code for IntegriteError exception.
    with open("./data/head-cust.csv", "rb") as content:
        next(content)
        lines = content.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines[:-1]:
            cdb.populate_database(line)

    # Assert recrods are present.
    with open("./data/head-cust.csv", "rb") as content:
        next(content)
        lines = content.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines[:-1]:
            customer = line.split(",")
            item = cdb.db.Customer.get(
                cdb.db.Customer.customer_id == customer[0]
            )
            print(item.customer_id)
            assert item.customer_id == customer[0]
            assert item.name == customer[1]
            assert item.last_name == customer[2]
            assert item.home_address == customer[3]
            assert item.phone_number == customer[4]
            assert item.email_address == customer[5]
            assert item.status.lower() == customer[6].lower()
            assert int(item.credit_limit) == int(customer[7])

    # Cleanup database.
    with open("./data/head-cust.csv", "rb") as content:
        next(content)
        lines = content.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines[:-1]:
            customer = line.split(",")
            query = cdb.db.Customer.delete().where(
                cdb.db.Customer.customer_id == customer[0]
            )
            assert bool(query.execute()) is True


def test_main(caplog):
    """Test main function
    """
    caplog.set_level(logging.INFO)
    cdb.main(["-i", "./data/head-cust.csv"])
    output = [record for record in caplog.records]
    assert "Parsing command line arguments..." in str(output)
    assert "Initializes the HP Norton database from csv" in str(output)
    assert "Adding tables..." in str(output)
    assert "Adding record for C000000" in str(output)
    assert "Adding record for C000001" in str(output)
    assert "Adding record for C000002" in str(output)
    assert "Adding record for C000003" in str(output)
    assert "Adding record for C000004" in str(output)
    assert "Adding record for C000005" in str(output)
    assert "Adding record for C000006" in str(output)
    assert "Adding record for C000007" in str(output)
    assert "Adding record for C000008" in str(output)
    assert "End of file" in str(output)
    assert "Closing database" in str(output)

    with open("./data/head-cust.csv", "rb") as content:
        next(content)
        lines = content.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines[:-1]:
            customer = line.split(",")
            item = cdb.db.Customer.get(
                cdb.db.Customer.customer_id == customer[0]
            )
            assert item.customer_id == customer[0]
            assert item.name == customer[1]
            assert item.last_name == customer[2]
            assert item.home_address == customer[3]
            assert item.phone_number == customer[4]
            assert item.email_address == customer[5]
            assert item.status.lower() == customer[6].lower()
            assert int(item.credit_limit) == int(customer[7])

    # Cleanup database
    with open("./data/head-cust.csv", "rb") as content:
        next(content)
        lines = content.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines[:-1]:
            customer = line.split(",")
            query = cdb.db.Customer.delete().where(
                cdb.db.Customer.customer_id == customer[0]
            )
            assert bool(query.execute()) is True
        # assert False
