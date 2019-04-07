Notes on assignment:

We have here two sets of tests, one written in unittest and the other in pytest.
I had originally wanted to do this with pytest but ran into some hurdles, so I
coded it using unittest.  Later I figgured out what my issue was and coded
another set of tests using pytest.  Both test suites are running nearly
identical tests.  Both sets of test cover 100% of the inventory management code
and 92% of the main code, missing only the if name is main section.

Following are the commands I would execute for testing.
All commands are run from the root project folder (./assignment/)
Pylint returns 10/10 for all code, tests included, using included pylintrc

```
pytest --cov=./inventory_management ./pytests
pytest --cov=main ./pytests

python -m coverage run --source=inventory_management -m unittest discover
coverage report
python -m coverage run --source=main -m unittest discover
coverage report

pylint pytests/
pylint unittests/
pylint inventory_management/
pylint main
```



Grading
=======

For assignment 1, you will need to supply your own unit_tests.py 
and integration_test.py files.

The assignment is graded as follows:
1. Run the student unit_tests
2. Run coverage and linting using the regular batch file
