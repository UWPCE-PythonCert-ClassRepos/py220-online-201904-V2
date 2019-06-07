'''
Lesson 09 Activity
Context Manager for Ballard Lockes
'''

# pylint: disable-msg=unnecessary-pass

class CapacityError(Exception):
    '''
    Custom error raised if too many boats try to enter the lock.
    '''
    pass


class Locke:
    '''
    Context manager class to simulate the overall functioning of the Ballard
    Locks.
    '''

    def __init__(self, max_boats):
        '''
        Initializes the class with the max number of boats that the lock can
        handle.
        '''
        self.max_boats = max_boats

    def __enter__(self):
        '''
        Enters the context manager and opens the lock.
        :return: self
        '''
        print('Stopping the pumps.')
        print('Opening the doors.')
        return self

    def move_boats_through(self, num_boats):
        '''
        Checks number of boats against locke capacity.
        :param num_boats: number of boats
        '''
        if num_boats > self.max_boats:
            raise CapacityError('There are too many boats.')
        print('Closing the doors.')
        print('Restarting the pumps.')
        print(f'{num_boats} boats are going through the lock.')
        print('Stopping the pumps.')
        print('Opening the doors.')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Closing the doors.')
        print('Restarting the pumps.')

        if exc_type:
            print(f'Exception Type: {exc_type}')
            print(f'Exception Value: {exc_val}')
            print(f'Exception Traceback: {exc_tb}')


if __name__ == '__main__':

    SMALL_LOCKE = Locke(5)
    LARGE_LOCKE = Locke(10)

    BOATS = 8

    # A locke with sufficient capacity can move boats without incident.
    print('LARGE BALLARD LOCKE')
    try:
        with LARGE_LOCKE as locke:
            locke.move_boats_through(BOATS)
    except CapacityError:
        print(f'Error: {BOATS} boats will not fit in this lock.')

    # Too many boats through a small locke will raise an exception.
    print('\nSMALL BALLARD LOCKE')
    try:
        with SMALL_LOCKE as locke:
            locke.move_boats_through(BOATS)
    except CapacityError:
        print(f'Error: {BOATS} boats will not fit in this lock.')
