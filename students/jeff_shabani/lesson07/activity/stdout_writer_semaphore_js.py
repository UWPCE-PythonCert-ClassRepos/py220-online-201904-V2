import random
import sys
import threading
import time
from pysnooper import snoop

lock = threading.Lock()

sema = threading.Semaphore()


def write():
    sema.acquire()
    sys.stdout.write("%s writing.." % threading.current_thread().name)
    time.sleep(random.random())
    sys.stdout.write("..done\n")
    sema.release()


threads = []
for i in range(5):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    threads.append(thread)
    time.sleep(.1)

for thread in threads:
    thread.join()
