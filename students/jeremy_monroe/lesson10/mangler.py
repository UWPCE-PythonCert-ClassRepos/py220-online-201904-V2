#!/usr/bin/env python3

"""
Simple metaclass example that creates upper and lower case versions of
all non-dunder class attributes
"""


class NameMangler(type):  # deriving from type makes it a metaclass.
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance

    def __new__(cls, clsname, bases, _dict):
        uppercase_attr = {}
        for name, val in _dict.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
                uppercase_attr[name.lower()] = val

                name_doubled = name+name
                uppercase_attr[name_doubled] = val
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
    print(f.X)
    print(f.y)
    print(f.Y)
    print(f.xx)
    g = Foo()
    print(g.xx)
    print(g.X)
    print(id(f))
    print(id(g))
    assert id(f) == id(g)

    b = Bar()
    b.A_METHOD()
