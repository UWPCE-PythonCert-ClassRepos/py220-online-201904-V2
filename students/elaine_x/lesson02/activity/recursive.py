"""
recursion for debuging
"""

import sys


def my_fun(n):
    # if n < 1:
        #return False
    if n == 2:
        return True

    return my_fun(n / 2)


if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_fun(n))


'''
1. What is wrong with our logic?
If the number is power of 2, then the function yields "True".
If the number is odd, then the function keeps calling itself and calling itself and the number
keeps on getting smaller and smaller and it doesn't know to stop.

2. Why doesn't the function stop calling itself?
There is no condition to stop the function and return "False" when the number is not power of 2.

3. What's happening to the value of 'n' as the function gets deeper and deeper into recursion?
The number keeps on getting smaller and smaller and it doesn't know to stop.


Below is my debugging log:

Last login: Sat Apr 13 19:15:22 on ttys001
elaines-MacBook-Air:activity elaine$ cat recursive.py 
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
    print(my_fun(n))
elaines-MacBook-Air:activity elaine$ python3 recursive.py 2
True
elaines-MacBook-Air:activity elaine$ python3 recursive.py 4
True
elaines-MacBook-Air:activity elaine$ 3
-bash: 3: command not found
elaines-MacBook-Air:activity elaine$ python3 recursive.py 3
Traceback (most recent call last):
  File "recursive.py", line 16, in <module>
    print(my_fun(n))
  File "recursive.py", line 11, in my_fun
    return my_fun(n / 2)
  File "recursive.py", line 11, in my_fun
    return my_fun(n / 2)
  File "recursive.py", line 11, in my_fun
    return my_fun(n / 2)
  [Previous line repeated 994 more times]
  File "recursive.py", line 9, in my_fun
    if n == 2:
RecursionError: maximum recursion depth exceeded in comparison
elaines-MacBook-Air:activity elaine$ python3 -m pdb recursive.py 15
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(3)<module>()
-> """
(Pdb) l
  1  	"""
  2  	recursion for debuging
  3  ->	"""
  4  	
  5  	import sys
  6  	
  7  	
  8  	def my_fun(n):
  9  	    if n == 2:
 10  	        return True
 11  	    return my_fun(n / 2)
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(5)<module>()
-> import sys
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(8)<module>()
-> def my_fun(n):
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(14)<module>()
-> if __name__ == '__main__':
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(15)<module>()
-> n = int(sys.argv[1])
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(16)<module>()
-> print(my_fun(n))
(Pdb) pp n
15
(Pdb) ll
  1  	"""
  2  	recursion for debuging
  3  	"""
  4  	
  5  	import sys
  6  	
  7  	
  8  	def my_fun(n):
  9  	    if n == 2:
 10  	        return True
 11  	    return my_fun(n / 2)
 12  	
 13  	
 14  	if __name__ == '__main__':
 15  	    n = int(sys.argv[1])
 16  ->	    print(my_fun(n))
 17  		
(Pdb) s
--Call--
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(8)my_fun()
-> def my_fun(n):
(Pdb) ll
  8  ->	def my_fun(n):
  9  	    if n == 2:
 10  	        return True
 11  	    return my_fun(n / 2)
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(9)my_fun()
-> if n == 2:
(Pdb) pp n
15
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(11)my_fun()
-> return my_fun(n / 2)
(Pdb) s
--Call--
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(8)my_fun()
-> def my_fun(n):
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(9)my_fun()
-> if n == 2:
(Pdb) pp n
7.5
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(11)my_fun()
-> return my_fun(n / 2)
(Pdb) s
--Call--
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(8)my_fun()
-> def my_fun(n):
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(9)my_fun()
-> if n == 2:
(Pdb) pp n
3.75
(Pdb) ll
  8  	def my_fun(n):
  9  ->	    if n == 2:
 10  	        return True
 11  	    return my_fun(n / 2)
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(11)my_fun()
-> return my_fun(n / 2)
(Pdb) s
--Call--
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(8)my_fun()
-> def my_fun(n):
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(9)my_fun()
-> if n == 2:
(Pdb) pp n
1.875
(Pdb) ll
  8  	def my_fun(n):
  9  ->	    if n == 2:
 10  	        return True
 11  	    return my_fun(n / 2)
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(11)my_fun()
-> return my_fun(n / 2)
(Pdb) s
--Call--
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(8)my_fun()
-> def my_fun(n):
(Pdb) n
> /Users/elaine/PycharmProjects/Giraffe/Python_220/py220-online-201904-V2/students/elaine_x/lesson02/activity/recursive.py(9)my_fun()
-> if n == 2:
(Pdb) pp n
0.9375
(Pdb) 


'''