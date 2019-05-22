import threading
import time

lock = threading.Lock()


def f():
    lock.acquire()
    print("%s got lock" % threading.current_thread().name)
    time.sleep(1)
    print("%s done" % threading.current_thread().name)
    lock.release()


threading.Thread(target=f).start()
threading.Thread(target=f).start()
threading.Thread(target=f).start()
