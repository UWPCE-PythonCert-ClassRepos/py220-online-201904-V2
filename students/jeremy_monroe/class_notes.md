# Week 1



## Advanced Testing

#### New words, concepts, tools

- unittest
- unittest.TestCase
- dependency injection
- TestCase.setUp
- mock
- mock.MagicMock
- flake8
- pylint
- coverage

#### Unittest

Unittest tests go in a class that inherits from unittest.TestCase.

tests then go inside methods in that class and start with test_.

Assertions are made using `self.assertEqual()` which takes two arguments to compare and an optional third that can display a helpful message.

```python
import unittest
from squarer import Squarer

class SquarerTest(unittest.TestCase):
	def test_positive_numbers(self):
		
```

Finally, to run the tests the file will be run through `unittest`, you can't just run the file. So in cmd prompt:

`python -m unittest test2`



#### Unittesting calculator class on its own

we can use the `unittest` subclass `mock` to test whether our classes methods are called with the proper arguments in the proper order. We'll import `MagicMock` from `unittest.mock`:

```python
from unittest.mock import MagicMock
```

Then, in `CalculatorTests` after initializing instances of `adder, subtractor, multiplier, divider` and an instance of `calculator` we'll create the `test_adder_call` method:

```python
def test_adder_call(self):
    self.adder.calc = MagicMock(return_value=0)
    
    self.calculator.enter_number(1)
    self.calculator.enter_number(2)
    self.calculator.add()
    
    self.adder.calc.assert_called_with(1, 2)
```

First we override `adder`'s `.calc` method with `MagicMock` telling it to always return zero.

Then we add numbers to our stack as usual and call `calculator.add`. MagicMock will store information about the method call including what order the arguments were passed in.

`assert_called_with` is a `unittest.mock` special method and checks the order of the arguments, in this case the arguments passed to `adder.calc`.



#### Integration Testing

Didn't cover much that needed notes.



#### Coverage Testing

`pip install coverage`

To use coverage. In command prompt in the directory you want to test coverage:

`coverage run -m unittest test_script_filename`

then:

`coverage report`

Or you can run specific tests. In the case of `test_unit` in the calculator activity:

`coverage run --source=calculator -m unittest test_unit.AdderTest test_unit.SubtracterTest`

↑ if we don't include `--source=calculator` then the `test_unit.py` file will be included in the coverage test. We don't want that since we're testing individual tests from within that file.

Using `coverage report -m` will tell us exactly which lines were missed in our coverage.

Also, we can generate an html version of the report using `coverage html`

This will create an `htmlcov` directory. On windows in command prompt we can use:

`start htmlcov/index.html`

to open this in a web browser.





# Week 2

### Logging

logging levels are:

* Critical
* Error
* Warning
* Info
* Debug

logging does have to be imported: `import logging`

Set logging level using:

`logging.basicConfig(level=logging.WARNING)`

warning is the default level.

In your code add log messages simply with:

`logging.error("example log error")`

if the log level is higher than the set level it will be logged.

Next we'll set up `log_format` so our logs will provide us with more information:

`log_format  = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"`



Once we have our log messages formatted more prettily we can specify to save them to another file for later review. We'll add to the `logging.basicConfig`:

`logging.basicConfig(level=logging.WARNING, format=log_format, filename='mylog.log')`

The file `mylog.log` will be created in the cwd. If the python script is run repeatedly the log will be appended with the later log messages.

#### More complicated better logging config

Ok, to improve on our original setup we have to take a deeper dive into `logging`

We'll leave `log_format` in place and replace `logging.basicConfig` with:

```python
# Create a "formatter" using our format string
formatter = logging.Formatter(log_format)

# Create a log message handler that sends output to the file 'mylog.log'
file_handler = logging.FileHandler('mylog.log')
file_handler.setFormatter(formatter)

# get the 'root' logger
logger = logging.getLogger()
# Add our file_handler to the 'root' logger's handlers.
logger.addHandler(file_handler)
```

This is still a fairly basic setup. To mix things up let's say we want to send only log messages above level `WARNING` to our log file but send every log message to the console. It would look like this:

```python
# we're still using the log_format variable we defined earlier
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler('mylog.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
# We set the logging level for each handler above and then set it here too. If we didn't set the logger level here it would default to WARNING and wouldn't send log messages lower than that to either handler.
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHanlder(console_handler)
```

Super.



### Debugging

We'll use `pdb`, the built in Python debugging module to start. To debug a file use:

`python3 -m pdb my_file.py`

Once `pdb` is running your file some basic commands are:

* `?` - help
* `n` - next
* `s` - step into a function call
* `l` - list, show where you are in the file
* `b` - set a break point
* `condition 1` - would set a condition for breakpoint 1.
* `c`, `cont`, or `continue` - run code until breakpoint is reached
* `disable 1` - will disable breakpoint 1

To set a breakpoint first set the breakpoint, then define the condition when the breakpoint will come into effect:

`b 15` will set a breakpoint at line 15

`condition 1 i > 700` sets a condition for breakpoint 1 so that the code will run until that condition is reached.



# Week 3

peewee. `pip install peewee`

To start, instantiate a database and models:

```python
from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
	name = CharField()
	birthday = DateField()
	
	class Meta:
		database = db # This model uses the 'people.db' database
        
class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()
    
    class Meta:
        database = db # This model uses the 'people.db' database
```

The pet model is related to the person model through a foreign key relationship.

It's not necessary to open the database connection explicitly but it's good practice:

`db.connect()`

Then we create our tables:

`db.create_tables([Person, Pet])`

A couple different ways to store data:

```python
from datetime import date
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 2))
uncle_bob.save()

# or

grandma = Person.create(name='Grandma', birthday=date(1925, 2, 15))

# update a row:
grandma.name = "Grandma L."
grandma.save()
```



Next we'll add pets:

```python
bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
```

and delete pets:

`herb_fido.delete_instance()`

### Peewee retrieving data

to get a single record use `select.get()`:

` grandma = Person.select().where(Person.name == 'Grandma L.').get()`

or

`grandma = Person.get(Person.name == 'Grandma L.')`

To get all the people:

`people = Person.select()`

To get all the people and their pets:

`query = (Pet.select(Pet, Person).join(Person).where(Pet.animal_type =='cat'))`

Sort queries with `order_by`:

`people = Person.select().order_by(Person.birthday.desc())`

To get all people with their pets attached we use `prefetch`:

`query = Person.select().order_by(Person.name).prefetch(Pet)`

To search for anyone whose name starts with an upper or lowercase G we'll use a SQL function:

```python
expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
for person in Person.select().where(expression):
	print(person.name)
	
# prints:
# Grandma L.
```

Finally we'll close the connection:

`db.close()`