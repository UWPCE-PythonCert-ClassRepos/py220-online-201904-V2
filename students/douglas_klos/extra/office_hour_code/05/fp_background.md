FROM Function Programming in Python
===================================
https://www.packtpub.com/application-development/functional-python-programming-second-edition

---

Functional programming is an approach to programming that focuses more on using function definitions to process data than state change and mutable objects. This tends to create programs that are more succinct and expressive.

---

What are other approaches to programming?

---

Python has numerous functional programming features. It is not a purely a functional programming language. It offers enough of the right kinds of features that it confers the benefits of functional programming.

---

In a functional language, we replace the state—the changing values of variables—with a simpler notion of evaluating functions. Each function evaluation creates a new object or objects from existing objects. Since a functional program is a composition of functions, we can design lower-level functions that are easy to understand, and then design higher-level compositions that can also be easier to visualize than a complex sequence of statements.

---

OO:
```
class Summable_List(list):
    def sum(self):
        s = 0
        for v in self:
            s += v
        return s
```

---

FP:
```
def sumr(seq):
    if len(seq) == 0: return 0
    return seq[0] + sumr(seq[1:])
```

---

We can achieve expressive, succinct programs using higher-order functions. These are
functions that accept a function as an argument or return a function as a value. We can use
higher-order functions as a way to create composite functions from simpler functions.

---

Since we're not using variables to track the state of a computation, our focus needs to stay
on immutable objects. We can make extensive use of tuples and namedtuples to provide
more complex data structures that are immutable. Strings are also immutable of course and can be used.

---

Functional programs don't rely on loops and the associated overhead of tracking the state of
loops. Instead, functional programs try to rely on the much simpler (computationally, not conceptually) approach of recursive functions. BTW, to understand recursion fully, you first have to first understand recursion.

---

```
def isprimer(n: int) -> bool:
    def isprime(k: int, coprime: int) -> bool:
        """Is k relatively prime to the value coprime?"""
        if k < coprime*coprime: return True
        if k % coprime == 0: return False
        return isprime(k, coprime+2)
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    return isprime(n, 3)
```

---

A function with no side effects fits the pure mathematical abstraction of a function: there are
no global changes to variables. If we avoid the global statement, we will almost meet this
threshold. To be pure, a function should also avoid changing the state mutable objects.

---

Here's an example of a pure function:

```
def m(n: int) -> int:
    return 2**n-1
```

---

This result depends only on the parameter, n. There are no changes to global variables and
the function doesn't update any mutable data structures.

Any references to values in the Python global namespace (using a free variable) is
something we can rework into a proper parameter.  

---

We can't easily eliminate all stateful Python objects. Therefore, we must strike a balance
between managing state while still exploiting the strengths of functional design. Toward
this end, we should always use the with statement to encapsulate stateful file objects into a
well-defined scope.

---

Currying
========

```
from pymonad import curry
@curry
def systolic_bp(bmi, age, gender_male, treatment):
    return (
        68.15+0.58*bmi+0.65*age+0.94*gender_male+6.44*treatment
    )

>>> systolic_bp(25, 50, 1, 0)
116.09
>>> systolic_bp(25, 50, 1, 0)
122.53
```

---

```
>>> treated = systolic_bp(25, 50, 0)
>>> treated(0)
116.09
>>> treated(1)
122.53

```

---

Functional programming emphasizes stateless objects. In Python, this leads us to work with
generator expressions, generator functions, and iterables, instead of large, mutable,
collection objects. The itertools library has numerous functions to help us work with iterable sequences of objects, as well as collection objects.

---

These functions behave as if they are proper, lazy, Python iterables. Some
of them create intermediate objects, however; this leads to them
consuming a large amount of memory. Since implementations may change
with Python releases, we can't provide function-by-function advice here. If
you have performance or memory issues, ensure that you check the
implementation.

---

There are a large number of iterator functions in the itertools module. There are 3 groups:

---

Functions that work with infinite iterators. These can be applied to any iterable or
an iterator over any collection. For example, the enumerate() function doesn't
require an upper bound on the items in the iterable.
    count(): This is an unlimited version of the range() function
    cycle(): This will reiterate a cycle of values
    repeat(): This can repeat a single value an indefinite number of times

---    
    
Functions that work with finite iterators. These can either accumulate a source
multiple times, or they produce a reduction of the source. For example, grouping
the items produced by an iterator requires an upper bound.
chain(): This function combines multiple iterables serially.
groupby(): This function uses a function to decompose a single iterable into a
sequence of iterables over subsets of the input data.

---

    zip_longest(): This function combines elements from multiple iterables. The
    built-in zip() function truncates the sequence at the length of the shortest
    iterable. The zip_longest() function pads the shorter iterables with the given
    fill value.
    compress(): This function filters one iterable based on a second iterable of
    Boolean values.
    islice(): This function is the equivalent of a slice of a sequence when applied to
    an iterable.

---    
    
The tee iterator function clones an iterator into several copies that can each be
used independently. This provides a way to overcome the primary limitation of
Python iterators: they can be used only once.
