"""
    You will submit two modules: linear.py and parallel.py
    Each module will return a list of tuples, one tuple for
     customer and one for products.
    Each tuple will contain 4 values: the number of records processed,
    the record count in the database prior to running, the record count
    after running,
    and the time taken to run the module.

"""

import pytest
import src.database_operations as l


@pytest.fixture
def _linear_answers():
    """ Pytest fixture for linear insertion results """

    linear_answers = l.linear(
        ["./data/customer.csv", "./data/product.csv", "./data/rental.csv"]
    )


     
@pytest.fixture
def _parallel_answers():
    """ Pytest fixture for parallel insertion results """

    parallel_answers = l.parallel(
        ["./data/customer.csv", "./data/product.csv", "./data/rental.csv"]
    )


def test_linear(_linear_answers):
    # linear cust/prod, parallel cust/prod
    for answer in _linear_answers:
        print(f"answer:{answer}")

    assert False
        
        
        # needs a few more
        # assert type(answer["success"]) == int
        # assert type(answer["fail"]) == int
        # assert type(answer["total_records"]) == int
        # assert type(answer["elapsed"]) == float
        # assert answer["elapsed"] > 0.0


def test_parallel(_parallel_answers):
    pass
