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