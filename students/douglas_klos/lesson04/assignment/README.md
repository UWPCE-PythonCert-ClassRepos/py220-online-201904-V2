*** Lesson 04

For lesson 04 I primarily altered the create_db.py file.  It now uses a
generator to feed the csv file one line using a list comprehension into
the populate_database function.

For the basic_operations.py there wasn't much that I could do, the majority of
the code in that file is peewee calls to the database - the iteration of
records is done in the test file.

Please note that since this is a continuation of lesson 03, a lot of the
information below is still relevant, particularly the file layout.

*** Lesson 03

For this assignment we have completed two separate implementations
of the requested functions, one using Peewee and the other using
SQLAlchemy.  Each implementation function independently of each other.

```
assignment
├── peewee
│    ├─── data - databases and csv files
│    ├─── src - main python code
│    └─── tests - pytest files
└─── sqlalchemy
     ├─── data - databases and csv files
     ├─── src - main python code
     └─── tests - pytest files
```

The data folder contains the following files, these allowed me to 
quickly reset the database to different states with a cp.
```
customer.csv - Full HP Norton database in CSV format.
head-cust.csv - Top ten lines, or head, or customer.csv.
HPBlank.db - Database containing only an empty table.
HPHead.db - Database containing the top ten lines from the customer.csv.
HPNorton.dp - Full csv database imported into SQLite3.
```


The src folder contains the following files:
```
basic_operation.py - The functions required by the assignment.
db_model.py - The class definition for the sql table.
create_db.py - One off program to seed the customer.csv file into HPNorton.dp.
```

Tests were run from the root of the project, example below.  Tests are designed
to cleanup after themselves, but if failures happen it is a good idea to
copy over a blank database, the reset.sh script can help with this.
Tests are designed to cover basic_operations.py and dm_model.py.  The program
create_db.py is a one off program to seed the database and as such I did not
feel the need to spend time testing it.

Note that if you try to run both tests by calling pytest on the directory, the
second test often fails for reasons unknown to me.  Both tests can be run
back to back without problem though as long as they're run separately.

```
$ pwd
./py220-online-201904-V2/students/douglas-klos/lesson04/assignment/peewee/
$ ./reset.sh
$ pytest --cov=src --cov-report html ./tests/test_basic_operations.py
$ pytest --cov=src --cov-report html ./tests/test_gradel04.py
```

A new copy of the HPNorton database can be generated as following.
```
$ ./src/create_db.py -i data/customer.csv
```

A new blank database can be created with:
```
$ ./src/create_db.py -i data/customer.csv -b
```

My conclusion after doing both of these, Peewee is certainly easier to use, 
while SQLAlchemy has significantly more options to play with.  For work on a
small database that isn't handling a tremendous amount of requests Peewee seems
like a perfectly reasonable option.  If you're working on the back end for a
large database or one with numerous requests / connections, SQLAlchemy is likely
the better option.  Either way, it was a good exercise to practice both.