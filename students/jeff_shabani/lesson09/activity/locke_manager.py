#!/usr/bin/env python3

from contextlib import contextmanager
import typing


class Locke:
    def __init__(self, capacity: int, name=None):
        self.capacity = capacity

    def __enter__(self):
        return self

    def stop_pumps(self):
        print('Stopping the pumps')
        return self

    def restarting_pumps(self):
        print("Restarting the pumps")
        return self

    def open_doors(self):
        print("Opening the doors")
        return self

    def close_doors(self):
        print("Closing the doors")

    def move_boats_through(self, boats: int, boat_name):
        self.boats = boats
        self.boat_name = boat_name
        if self.boats <= self.capacity:
            self.stop_pumps()
            self.open_doors()
            self.close_doors()
            self.restarting_pumps()
        else:
            print(f'Boat {self.boat_name} {boats} exceeds capacity {self.capacity}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print('__exit__called')
            print(f'exec_type: {exc_type}')
            print(f'exec_val: {exc_val}')
            print(f'exec_traceback: {exc_tb}')


if __name__ == '__main__':
    small_locke = Locke(7)
    large_locke = Locke(12)
    sm_boat = 3
    med_boat = 9
    big_boat = 13

    try:
        with small_locke as locke:
            locke.move_boats_through(sm_boat, 'small boat')
    except:
        raise Exception('exception raised:small boat / small lock').with_traceback(None)

    try:
        with large_locke as locke:
            locke.move_boats_through(big_boat, 'big_boat')
    except:
        raise Exception('exception raised:small boat / small lock').with_traceback(None)
