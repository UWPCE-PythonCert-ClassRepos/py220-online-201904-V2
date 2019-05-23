import random
import sys
import threading
import time


LOCK = threading.Lock()


def write():
    '''
    Adding a locking mechanism to compartmentalize the stdout method to
    individual threads
    '''
    with LOCK:
        sys.stdout.write("%s writing.." % threading.current_thread().name)
        time.sleep(random.random())
        sys.stdout.write("..done\n")

THREADS = []

for i in range(20):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    THREADS.append(thread)
    time.sleep(.1)

for i in THREADS:
    i.join()

'''
eve:activity jmiller$ python stdout_writer_semaphore.py
Thread-1 writing..Thread-2 writing....done
Thread-3 writing....done
Thread-4 writing....done
Thread-5 writing....done
Thread-6 writing....done
Thread-7 writing....done
Thread-8 writing....done
Thread-9 writing....done
..done
Thread-11 writing..Thread-10 writing....done
Thread-12 writing....done
Thread-13 writing....done
Thread-14 writing....done
Thread-15 writing....done
Thread-16 writing....done
Thread-17 writing....done
Thread-18 writing....done
Thread-19 writing....done
Thread-20 writing....done
Thread-21 writing....done
Thread-22 writing....done
Thread-23 writing....done
Thread-24 writing....done
Thread-25 writing....done
..done
[master]
'''
