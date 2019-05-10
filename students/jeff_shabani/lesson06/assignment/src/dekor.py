import time
from functools import wraps, update_wrapper

def tot_today(func_to_dekorate):
    def wrapper(*args, **kwargs):
        print("total budget today:")
        result = func_to_dekorate(*args, **kwargs)
        #do noen ting etter
        return result
    return wrapper

def tot_yest(func_to_dekorate):
    def wrapper(*args, **kwargs):
        print("total budget yesterday:")
        result = func_to_dekorate(*args, **kwargs)
        #do noen ting etter
        return result
    return wrapper

def tot_param (m,t):
    def dekorator(func):
        def wrapper(*args, **kwargs):
            print("total",m, t,":")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return dekorator

def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        end = time.perf_counter()
        run_time=end - start
        print(f'Process {f.__name__!r} runs in {run_time} seconds.')
        return result
    return wrapper

class CountCalls:
    def __init__(self, func):
        update_wrapper(self,func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls +=1
        print(f'Call {self.num_calls} of {self.func.__name__!r}')
        return self.func(*args, **kwargs)