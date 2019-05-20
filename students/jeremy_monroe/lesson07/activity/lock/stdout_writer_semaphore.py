import random
import sys
import threading
import time

lock = threading.Semaphore(1)

def write():
    lock.acquire()
    sys.stdout.write("%s writing.." % threading.current_thread().name)
    time.sleep(random.random())
    sys.stdout.write("..%s done\n" % threading.current_thread().name)
    lock.release()


# while True:
for _ in range(10):
    thread = threading.Thread(target=write)
    thread.start()
    time.sleep(.1)

