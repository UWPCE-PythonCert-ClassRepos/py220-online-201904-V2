For this assignment we have completed two seperate implementations
of the requested functions, one using Peewee and the other using
SQLAlchemy.

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

Tests were run from the root of the project, such as.  Tests are designed
to cleanup after themselves, but if failures happen it is a good idea to
copy over a blank database, the reset.sh script can help with this.
```
$ pwd
./py220-online-201904-V2/students/douglas-klos/lesson03/assignment/peewee/
$ pytest --cov=src --cov-report html ./tests/
```

