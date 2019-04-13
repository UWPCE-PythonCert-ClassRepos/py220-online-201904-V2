"""
recursion for debuging
"""

import sys

def my_fun(n):
    if n == 2:
        return True
    return my_fun(n / 2)


if __name__ == '__main__':
    n = int(sys.argv[1])
#    import pdb; pdb.set_trace()
    print(my_fun(n))

'''
-> if __name__ == '__main__':
(Pdb) next
> /Users/jmiller/School/Python_220/students/jesse_miller/lesson02/activity/recursive.py(16)<module>()
-> n = int(sys.argv[1])
(Pdb) next
IndexError: list index out of range
> /Users/jmiller/School/Python_220/students/jesse_miller/lesson02/activity/recursive.py(16)<module>()
-> n = int(sys.argv[1])
(Pdb) next
--Return--
> /Users/jmiller/School/Python_220/students/jesse_miller/lesson02/activity/recursive.py(16)<module>()->None
-> n = int(sys.argv[1])
(Pdb) next
IndexError: list index out of range
> <string>(1)<module>()->None

Well, I know this is the problem.  sys.argv[1] want's a directory.  sys.argv[0]
is our current running program.  If you open it with 'python recursive.py 24' you
get:

eve:activity jmiller$ python recursive.py 24
Traceback (most recent call last):
  File "recursive.py", line 18, in <module>
    print(my_fun(n))
  File "recursive.py", line 12, in my_fun
    return my_fun(n / 2)
  File "recursive.py", line 12, in my_fun
    return my_fun(n / 2)
  File "recursive.py", line 12, in my_fun
    return my_fun(n / 2)
  [Previous line repeated 995 more times]
  File "recursive.py", line 9, in my_fun
    if n == 2:
RecursionError: maximum recursion depth exceeded in comparison

This is happening because there's no limiter on the file at all.  Since our
recursion depth is 1000, it's safe to assume we're going higher.  We could
increase the recursion depth, but at that point we're risking a stack overflow.

Instead, we should limit the recussion.  Something like
'for i in range(1 len(sys.argv))' and limiting the input to 8 or lower should
do it.

'''
