#!/usr/bin/env python3

import threading
import time


# create a mutable object that is shared among threads
class shared:
    val = 1


lock = threading.Lock()


def func():
    lock.acquire()
    print("%s got lock" % threading.current_thread().name)
    y = shared.val
    time.sleep(0.00001)
    y += 1
    shared.val = y
    print("%s done" % threading.current_thread().name)
    lock.release()


threads = []
# with enough threads, there's sufficient overhead to
# cause a race condition
for i in range(100):
    thread = threading.Thread(target=func)
    # thread.daemon=True
    threads.append(thread)
    thread.start()
    # thread.join()

for thread in threads:
    thread.join()

print(shared.val)

time.sleep(0.00001)
print("%s done" % threading.current_thread().name)
print(shared.val)
