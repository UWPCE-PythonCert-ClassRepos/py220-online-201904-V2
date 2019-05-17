#!/usr/bin/env python3

import multiprocessing
import time
import os


def whoami(name):
    print(f"I'm {name}, in process {os.getpid()}")


def loopy(name):
    whoami(name)
    start = 1
    stop = 1000000
    for num in range(start, stop):
        print(f'\tNumber {num} of {stop}!')
        time.sleep(.5)


if __name__ == '__main__':
    whoami("main")
    p = multiprocessing.Process(target=loopy, args=("loopy"))
    p.start()
    time.sleep(5)
    p.terminate()
