## Lesson 05

For this assignment functions have been written that satisfy the test cases included with the assignment, these are included in src/database_operations.py.  Include in the assignment folder is main.py, a CLI argument based front end for database operations to be used outside of the testing environment.  

Following is the directory layout for the assignment
```
assignment/ - root program folder
├─── data/ - databases and csv files
├─── src/ - module code
└─── tests/ - pytest files
```

Following are examples of syntax used for executing main.py from the assignment folder.  The first loads just the customers.csv file found in the ./data/ directory into a MongoDB collection.  The second loads all three files into collections.  Please note that at a minimum you must first specifiy the data directory, followed by n number of csv files to be imported, where n > 1.  I could not find a clean way to use argparser to require n > 2 arguments for this, only n > 1 or n = 2.
```
$ ./main.py -i ./data/ customers.csv
$ ./main.py -i ./data/ customers.csv product.csv rental.csv
```
To delete the three collections (customers, product, rental) from MongoDB:
```
$ ./main.py -d
```
To show a list of all available products:
```
$ ./main.py -p
```
To show rentals for a specified product_id:
```
$ ./main.py -r prd002
$ ./main.py -r prd007
```
Logging is enabled be default for all functions.  Logging can be disabled with the -l flag:
```
$ ./main.py -l
```
Show the help menu for main.py:
```
$ ./main.py -h
```

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
