# Lesson 10 - Metaprogramming


## Layout

```
assignment/
   ├─── l05-decorator/ - HPNorton.py (Just a bunch of functions)
   │      ├─── data/ - csv files
   │      ├─── src/ - module code
   │      └─── tests/ - pytest file
   └─── l05-meta/ - HPNorton.py (Object Oriented with Metaclass)
          ├─── data/ - csv files
          ├─── src/ - module code
          └─── tests/ - pytest file
```

## Decorator

I first completed this assignment using a decorator - just consider it a warm up.

## Meta

Next I created an HPNorton class and moved all the database related function
calls to methods of the class.

From there I created a Context Manager class that is responsible for logging the
related information for functions / methods, such as time to complete, records
processed, args / kwargs, and when the function was called.  A basic decorator
function was then created using wrapt (to preserve introspection and signature)
that instantiates the context manager for the function / method being called.

Finally I created a metaclass that wraps each method of HPNorton with the
decorator function.

The tests are designed to be run on the smaller test data, which are a head
of the main larger data files.  Two scripts are included to facilitate
switching between the datasets.

Pylint _should_ be 10's for everything.  There have been some issues with
different environments yielding different pylint results, but it's all 10's
on my end.

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson10/assignment/l05-meta
$ ./data-test.sh
$ ./data-production.sh
```

Following is a list of commands used for the program:

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson10/assignment/l05-meta
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

There's also a srcript run_all_args.sh that executes every available option
for HPNorton.py.