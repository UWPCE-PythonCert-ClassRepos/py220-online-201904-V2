import threading
import time

lock = threading.Lock()

def f():
    lock.acquire()
    # with lock:
    print("%s got lock" % threading.current_thread().name)
    time.sleep(0.5)
    lock.release()

# threading.Thread(target=f).start()
# threading.Thread(target=f).start()
# threading.Thread(target=f).start()


for i in range(10):
    threading.Thread(target=f).start()
