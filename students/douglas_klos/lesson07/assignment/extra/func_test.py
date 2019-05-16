#!/usr/bin/env python3

# @Andy Miles You're probably at work, but a question for later.

# The None type is a useful placeholder, but itself is still an object that can be passed around.

# In the following example, we have a tuple of function calls and their parameters. We use a map call to then execute all functions in the list with their given parameters. This however passes the None object to g(), which is recognized as a parameter and gives a TypeError. The workaround I've found is for all functions that don't take parameters, to add *args to their list  to catch the None object map passes over.

# Is there any sort of object or placeholder that will still work in a data structure but when used or passed in this fashion would not break g's parameters, or is there a way to do a conditional in the function call, such as...
# ```x[0](x[1] if x[1] is not None else "PASS LITERALLY NOTHING")```

# I haven't found a way to do the pass nothing with an if-else yet.

POW = 2

def f(x):
    print(x**POW)

# def g(*args):
def g():
    global POW
    POW = 3

def main():
    function_list = ((f, 10), (g, None), (f, 10))
    list(map(lambda x: x[0](x[1]), function_list))

if __name__ == "__main__":
    main()
