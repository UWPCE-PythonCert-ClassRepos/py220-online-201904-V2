#!/usr/bin/env python3

"""
Simple metaclass example that creates upper and lower case versions of
all non-dunder class attributes
"""


class NameMangler(type):  # deriving from type makes it a metaclass.

    def __new__(cls, clsname, bases, _dict):
        uppercase_attr = {}
        for name, val in _dict.items():
            if not name.startswith('__'):
                name_upper = name.upper()
                name_lower = name.lower()
                uppercase_attr[name_upper] = val
                uppercase_attr[name_lower] = val
                uppercase_attr[name_upper+name_upper] = val
                uppercase_attr[name_lower+name_lower] = val

            else:
                uppercase_attr[name] = val

        return super().__new__(cls, clsname, bases, uppercase_attr)


class Foo(metaclass=NameMangler):
    x = 1
    Y = 2


# note that it works for methods, too!
class Bar(metaclass=NameMangler):
    x = 1

    def a_method(self):
        print("in a_method")


if __name__ == "__main__":
    f = Foo()
    print(f.x)
    print(f.xx)
    print(f.X)
    print(f.y)
    print(f.Y)
    print(f.YY)

    b = Bar()
    b.A_METHOD()
    b.A_METHODA_METHOD()
