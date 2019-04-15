I used unittest for unit test and integration test in this assignment.
Following are command I executed for testing and check the lint:

1. Pylint check:
python -m pylint ./inventory_management

Pylint  return 10/10

2. unit test with coverage
python -m coverage run --source=inventory_management -m unittest test_unit.py
..............
----------------------------------------------------------------------
Ran 14 tests in 0.014s

OK

3. integration test
python -m unittest test_integration.py

...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK


4.coverage
python -m coverage report

-----------------------------------------------------------------------
inventory_management\__init__.py                        0      0   100%
inventory_management\electric_appliances_class.py      11      0   100%
inventory_management\furniture_class.py                11      0   100%
inventory_management\inventory_class.py                13      0   100%
inventory_management\main.py                           51      3    94%
inventory_management\market_prices.py                   4      0   100%
-----------------------------------------------------------------------
TOTAL                                                  90      3    97%
