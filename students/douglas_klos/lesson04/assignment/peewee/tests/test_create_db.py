#pylint: disable=E0401, W0401
"""
    Tests for create_db.py
"""

from peewee import *
import create_db as cdb


def test_add_tables():
    """Test add_tables function
    """
    cdb.add_tables()
    fields = str(cdb.db.database.get_columns('Customer'))
    assert 'customer_id' in fields
    assert 'name' in fields
    assert 'last_name' in fields
    assert 'home_address' in fields
    assert 'phone_number' in fields
    assert 'email_address' in fields
    assert 'status' in fields
    assert 'credit_limit' in fields


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
    assert parser.input == './data/head-cust.csv'
    assert parser.blank is False
    parser = cdb.parse_cmd_arguments(["-i", "./data/head-cust.csv", "-b"])
    assert parser.blank is True
