*** Lesson 04

Again for lesson 04 we have a peewee and an sqlalchemy implementation of the
assignment, each running separately.  For this lesson I primarily altered the 
create_db.py file.  It now uses a generator to feed the csv file one line using
a list comprehension into the populate_database function.  I have also added
some test cases for create_db.py that weren't present in the l03 version.

For the basic_operations.py there wasn't much that I could do, the majority of
the code in that file is peewee/sqlalchemy calls to the database - the
iteration of records is done in the test file.  No changes were made to the
db_model.py file.

Following is a layout of the assignment files:
```
assignment
├───peewee
│    ├─── create_db.py - main program for seeding database.
│    ├─── data/ - databases and csv files
│    ├─── src/ - main python code
│    └─── tests/ - pytest files
└─── sqlalchemy
     ├─── create_db.py - main program for seeding database.
     ├─── data/ - databases and csv files
     ├─── src/ - main python code
     └─── tests/ - pytest files
```

The root folder contains:
```
create_db.py - One off program to seed the customer.csv file into HPNorton.db.
HPNorton.db - Database the program operates off of.
reset.sh - Script to reset database state.
```

The data folder contains the following files, these allowed me to quickly reset 
the database to different states with a copy (cp) command.
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
```

The test folder contains the following files:
```
test_gradel04.py - Grading tests given by instructor
test_basic_operations.py - Test file for basic operations
test_create_db.py - Test file for create_db.py (main program test)
```

Tests were run from the root of the project, example below.  Tests are designed
to cleanup after themselves, but if failures happen it is a good idea to
copy over a blank database, the reset.sh script can help with this.
Tests are designed to cover create_db.py, basic_operations.py, and dm_model.py
The following is an example from the peewee folder, commands are the same under
sqlalchemy.

```
$ pwd
./py220-online-201904-V2/students/douglas-klos/lesson04/assignment/peewee/
$ ./reset.sh
$ pytest --cov=src --cov-report html ./tests/test_basic_operations.py
$ pytest --cov=src --cov-report html ./tests/test_gradel04.py
$ pytest --cov=create_db --cov-report html ./tests/test_create_db.py
```

A new copy of the HPNorton database can be generated as following.
```
$ ./create_db.py -i data/customer.csv
```

A new blank database can be created with:
```
$ ./create_db.py -i data/customer.csv -b
```

My conclusion after doing both of these, Peewee is certainly easier to use, 
while SQLAlchemy has significantly more options to play with.  For work on a
small database that isn't handling a tremendous amount of requests Peewee seems
like a perfectly reasonable option.  If you're working on the back end for a
large database or one with numerous requests / connections, SQLAlchemy is likely
the better option.  Either way, it was a good exercise to practice both.