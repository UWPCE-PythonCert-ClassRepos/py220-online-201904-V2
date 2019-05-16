# Lesson 07 - Parallel Processing

I had during lesson 06 started working on a multi-process version of the
program. I have completed it and included it here with the requested lesson 05
code changes.

Following is the directory layout for the assignment:

```
assignment/
   ├─── l05/ - root program folder
   │      ├─── data/ - csv files
   │      ├─── src/ - module code
   │      └─── tests/ - pytest file
   └─── l06/ - root program folder
          ├─── data/ - .zip of dataset.csv file
          └─── src/ - module code
```

## Lesson 05 revisited

Implementing the multiprocessing for this was straight forward.  I already
had a wrapper function that would call insert for each file, I just made another
wrapper that does the same thing, except it spawns a new process for each one,
and then joins them after.  That part of the assignment took like 20-30 minutes.

Then came some heavy refactoring, abstraction, and redesign of the functions,
including introducing a Settings class to allow for easily changing the name of
the database you're connecting to.  Further, I came up with what I believe to be
a better way for my main function to handle a large number of command line
arguments, replacing my numerous if's with a loop and a list.  Also made good
use of map, filter, and lambda in some locations.

Included is a test suite that gives full coverage of the database_operations
code.  After finishing, I went back to the provided test_grade07.py to
implement it, but ended up deleting the file as its tests were pretty basic
compared to what had already been implemented, they added no new useful data.
The tests are designed to be run on the smaller test data, which are a head
of the main larger data files.  Two scripts are included to facilitate
switching between the datasets.
```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson07/assignment/l05
$ ./data-test.sh
$ ./data-production.sh
```

Following is a list of commands used for the program:
```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson07/assignment/l05
$ pylint ./src/
$ pylint ./tests/
$ pytest ./tests/
$ ./HPNorton.py -h
$ ./HPNorton.py --help
$ ./HPNorton.py --all-products
$ ./HPNorton.py --all-customers
$ ./HPNorton.py --all-rentals
$ ./HPNorton.py --available-products
$ ./HPNorton.py --drop-collections
$ ./HPNorton.py --drop-database
$ ./HPNorton.py --disable-log
$ ./HPNorton.py --rentals-for-customer C000001
$ ./HPNorton.py --customers-renting-product P000001
$ ./HPNorton.py --parallel ./data/customers.csv ./data/rental.csv ./data/product.csv
$ ./HPNorton.py --linear ./data/customers.csv ./data/rental.csv ./data/product.csv
```



## Lesson 06 revisited

Towards the end of lesson 06 I began playing with multiprocessing to speed up
to process of parsing the CSV file even more.  I've learned a lot in the past
few days since then and have improved the parallel version further.  The
code is still designed to execute under either python 2 or 3.

Commands used:
```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson07/assignment/l06
$ time ./src/parallel_v10.py
$ pylint ./src/
```
Included in the data folder is a .zip file of the dataset used for testing.
