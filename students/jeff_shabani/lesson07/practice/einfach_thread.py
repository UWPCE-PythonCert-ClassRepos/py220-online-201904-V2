#!/usr/bin/env python3

import sys
import threading
import time


# def func():
#     for i in range(5):
#         print(f'hello from {threading.current_thread().name}')
#         time.sleep(1)
#
#
# threads = []
# for i in range(3):
#     thread = threading.Thread(target=func, args=())
#     thread.start()
#     threads.append(thread)
#
# func()

lock = threading.Lock()

def f():
    lock.acquire()
    print("%s got lock" % threading.current_thread().name)
    time.sleep(.5)
    lock.release()


for i in range(10):

    threading.Thread(target=f).start()
# threading.Thread(target=f).start()
# threading.Thread(target=f).start()
# threading.Thread(target=f).start()

f()
