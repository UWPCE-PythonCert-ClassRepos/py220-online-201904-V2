## Lesson 05

For this assignment functions have been written that satisfy the test cases included with the assignment, these are included in src/database_operations.py.  Include in the assignment folder is main.py, a CLI argument based front end for database operations to be used outside of the testing environment.  

Following is the directory layout for the assignment
```
assignment/ - root program folder
├─── data/ - databases and csv files
├─── src/ - module code
└─── tests/ - pytest files
```

Following are examples of syntax used for executing main.py from the assignment folder.  Please note that at a minimum you must first specify the data directory, followed by n number of csv files to be imported, where n > 1.  I could not find a clean way to use argparser to require n > 2 arguments for this, only n > 1 or n = 2.

Show the help menu for main.py:
```
$ ./main.py -h
$ ./main.py --help
```
To show a list of all products:
```
$ ./main.py --all-products
```
To show a list of all customers:
```
$ ./main.py --all-customers
```
To show a list of all available products:
```
$ ./main.py --available-products
```
To delete the three collections (customers, product, rental) from MongoDB:
```
$ ./main.py --drop-collections
```
Logging is enabled be default for all functions but can be disabled:
```
$ ./main.py --disable-log
```
To show rentals for a specified user_id:
```
$ ./main.py --rentals-for-customer user005
```
To show customers renting a specified product_id:
```
$ ./main.py --customers-renting-product prd007
```
To load a single csv file into the MongoDB:
```
$ ./main.py --insert ./data/ customers.csv
```
To load multiple csv files into the MongoDB:
```
$ ./main.py --insert ./data/ customers.csv product.csv rental.csv
```
Please note that when inserting csv files, you must at a minimum specify the data directory, followed by N number of csv files to be imported, where N > 1.  I could not find a clean way to make argparser require N > 2 arguments, only N > 1 or N = X for X > 1.  I did however find an open issue on bugs.python.org relating to this lack of feature, issue11354. (https://bugs.python.org/issue11354)

Testing of the src files was done with the following syntax.  Note all test should be passing.  Currently main.py is not being tested, it only parses command line arguments and makes basic function calls.  If there's time it's something I'll implement.
```
$ pytest --cov=src ./tests/
$ pytest --cov=src --cov-report html ./tests/
```
Discovered the source of my constant E0401 pylint error.  Pylint is apparently
being run from outside of the virtual environment, even though 'which pylint'
specifies that it correctly running the pylint in the venv.  If I though
call it as a python module, no more E0401 issues.  Following are the various commands I used for linting the assignment:
```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson05/assignment
$ python -m pylint ./main.py
$ python -m pylint ./src/database_operations.py
$ python -m pylint ./src
```
