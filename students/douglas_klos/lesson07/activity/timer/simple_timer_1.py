#!/usr/bin/env python3

import threading
import datetime

def called_once():
    """
    this function is designed to be called once in the future
    """

    print("I just got called!  It's now: {}".format(time.asctime()))

# setting it up to be called
t = Timer(interval=3, function=called_once)
t.start()

# you can cancel if you want
t.cancel()
