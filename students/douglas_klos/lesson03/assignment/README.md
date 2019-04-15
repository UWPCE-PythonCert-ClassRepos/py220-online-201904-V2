For this assignment we have completed two seperate implementations
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
     ├─── src.rabbit.hole - First sqlalchemy attempt. Works, but a bit ugly.
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

```
$ pwd
./py220-online-201904-V2/students/douglas-klos/lesson03/assignment/peewee/
$ pytest --cov=src --cov-report html ./tests/
$ ./reset.sh; pytest --cov=src --cov-report html ./tests/
```

