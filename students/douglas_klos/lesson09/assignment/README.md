# Lesson 09

Folder layout

```
assignment/
   ├─── l02/ - charges_calc.py
   │      ├─── data/ - csv files
   │      └─── src/ - module code
   ├─── l05/ - HPNorton.py
   │      ├─── data/ - csv files
   │      ├─── src/ - module code
   │      └─── tests/ - pytest file
   └─── l09/
          ├─── data/ - csv files
          ├─── src/ - module code
          └─── tests/ - pytest file
```

## Decorators - Lesson 02 revisited

For this part of the assignment, I did a couple things.  Originally I had coded
it using the standard logging library, but lately have been using loguru with
fairly good results, so I recoded the assignment with the loguru library.

Second, I created a decorator, @disable_logging, that is placed before each
function that contains loguru calls.  When the program is executed from the
command line, if the '-d' flag is passed in, logging will be disabled.

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson09/assignment/l02/src/
$ pylint ./charges_calc.py
$ ./charges_calc.py -i ../data/source.json -o output.json
$ ./charges_calc.py -d -i ../data/source.json -o output.json
```


## Context Managers - Lesson 05 revisited

This is a continuation of the lesson05 changes made in lesson07.

For Lesson 05 I was already using a context manager for connecting to the
Mongo DB, but modified it to return a connection directily to the collection
I am using, instead of requiring an extra line to connect after starting
the context manager.  Further I sorted out a small error with the main file
that resulted in a crash when the program was called with no arguments.  It now
correctly displays the help menu.

The tests are designed to be run on the smaller test data, which are a head
of the main larger data files.  Two scripts are included to facilitate
switching between the datasets.

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson09/assignment/l05
$ ./data-test.sh
$ ./data-production.sh
```

Following is a list of commands used for the program:

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson09/assignment/l05
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

## Recursion

We covered recursion in the first week of the first class, I was a bit surprised
to see it again here towards the end of the second.

First, I rejected the name jpgdiscover since we're actually searching png files.
So it's called image_discover.py.

This was pretty straight forward, call the recursive function on the base path,
and for each directory it contains, call the function again on that subdir.
Repeat.  Each directory is checked for files whose extensions are checked
against valid ones and then appended to a list that is returned down the calls.

I also added the decorator from earlier in the assignment that allows you
to disable logging from the command line with the '-d' tag.

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson09/assignment/l09
$ pylint ./src/
$ pylint ./tests/
$ pytest ./tests/
$ ./src/image_discover.py --find ./data/
$ ./src/image_discover.py -d --find ./data/
$
$ # Same result as above, just from the src directory.
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson09/assignment/l09/src
$ ./image_discover.py --find ../data/
```