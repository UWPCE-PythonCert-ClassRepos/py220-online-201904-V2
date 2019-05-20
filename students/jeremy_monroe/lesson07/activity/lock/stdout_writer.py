import random
import sys
import threading
import time

LOCK = threading.Lock()


def write():
    LOCK.acquire()
    sys.stdout.write("%s writing.." % threading.current_thread().name)
    time.sleep(random.random())
    sys.stdout.write("..done\n")
    LOCK.release()


for i in range(100):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    time.sleep(.1)
