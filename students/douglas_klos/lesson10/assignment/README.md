# Lesson 10 - Metaprogramming


## Layout

```
assignment/
   ├─── l05-decorator/ - HPNorton.py
   │      ├─── data/ - csv files
   │      ├─── src/ - module code
   │      └─── tests/ - pytest file
   └─── l05-metaclass/ - HPNorton.py
          ├─── data/ - csv files
          ├─── src/ - module code
          └─── tests/ - pytest file
```

## Decorator

I first completed this assignment using a decorator - just consider it a warm up.

The tests are designed to be run on the smaller test data, which are a head
of the main larger data files.  Two scripts are included to facilitate
switching between the datasets.

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson10/assignment/l05-decorator
$ ./data-test.sh
$ ./data-production.sh
```

Following is a list of commands used for the program:

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson09/assignment/l05-decorator
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