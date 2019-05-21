#!/usr/bin/env python3

from functools import wraps
import time

def timer(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        end = time.perf_counter()
        run_time = end - start
        print(f'{run_time}')
        return result

    return wrapper