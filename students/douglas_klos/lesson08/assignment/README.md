# Lesson 08

## Closures and partials

This week though, the majority of time was spent working on a side project,
a fractal rendering program written in python with numba for jit compiling.
I've had a lot of fun writing it and it's working out better than I had
originally expected.

https://github.com/Douglas-Klos/fractals-py


### Commands used
```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson08/assignment/src
$ pylint ../tests/
$ pylint ./inventory/
$ pytest -vv ../tests/
$ pytest --cov=./inventory/ ../tests/
$ pytest --cov-report html --cov=./inventory/ ../tests/
$ firefox htmlcov/index.html
```

Pylint: 10 on all files

Pytest: 100% coverage of inventory.py