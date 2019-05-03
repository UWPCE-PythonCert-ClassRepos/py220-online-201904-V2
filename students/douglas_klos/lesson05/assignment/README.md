# Lesson 05

Once again, for lesson five, we have ended up with two completely separate implementations of the assignment, one using PyMongo and the other using MongoEngine.  Both implementations exceed the assignment requirements, and further pytest functions have been written to ensure 100% test coverage of the database code, in addition to instructor supplied tests.


Following is the directory layout for the assignment
```
assignment/
   ├───pymongo/ - root program folder
   │      ├─── data/ - csv and json files
   │      ├─── src/ - module code
   │      └─── tests/ - pytest files
   └───mongoengine/ - root program folder
          ├─── data/ - csv and json files
          ├─── src/ - module code
          └─── tests/ - pytest files
```
## main.py
Inside of each implementation is the exact same main.py file.  As both implementations are coded using the same function declarations, this cli based front-end is able to interact with both without any changes being made.  As such, all the following instructions are applicable to both implementations of the assignment.

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
To delete the entire HPNorton database:
```
$ ./main.py --drop-database
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
Please note that when inserting csv files, you must at a minimum specify the data directory, followed by N number of csv files to be imported, where N > 1.  I could not find a clean way to make argparser require N > 2 arguments, only N > 1 or N = X for X >= 1.  I did however find an open issue on bugs.python.org relating to this lack of feature, issue11354. (https://bugs.python.org/issue11354)

Testing of the src files was done with the following syntax.  Note all test should be passing.  Currently main.py is not being tested, it only parses command line arguments and makes basic function calls.  If I get super bored it's something I'll consider.
```
$ pytest --cov=src ./tests/
$ pytest --cov=src --cov-report html ./tests/
```
Finally discovered the source of my constant E0401 pylint error.  Pylint is apparently being run from outside of the virtual environment, even though 'which pylint' specifies that it's correctly running the pylint from the venv.  If though I call it as a python module, no more E0401 issues.  Following are the various commands I used for linting the assignment:
```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson05/assignment/pymongo
~/git/py220-online-201904-V2/students/douglas_klos/lesson05/assignment/mongoengine
$ python -m pylint ./main.py
$ python -m pylint ./src/database_operations.py
$ python -m pylint ./src
```

### PyMongo

PyMongo feels like the sqlite3 package of MongoDB, it's sorta clunky, and I feel like there's better solutions.  PyMongo seems quick and dirty, however it's effective.

### MongoEngine

Enter MongoEngine, a peewee equivalent in my above comparison.

MongoEngine appears to be based off of PyMongo and provides a sort of object-relational-mapping to MongoDB.

MongoEnging makes deprecated function calls into PyMongo, and as such pytest returns warnings each time these functions are called.  There's even a two year old open issue for it https://github.com/MongoEngine/mongoengine/issues/1491.  I got around this by dropping the entire collections instead of deleting records as a group.

As a whole, I found coding the assignment using MongoEngine and its mapper to be easier and more enjoyable than with PyMongo.
