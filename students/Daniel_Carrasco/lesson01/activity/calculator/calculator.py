"""
This module provides a custom calculator
"""


from .exceptions import InsufficientOperands


class Calculator:
    '''
    Class used to build the calculator
    '''

    def __init__(self, adder, subtracter, multiplier, divider):
        '''
        initializes variables
        '''
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        '''
        stores the numbers entered, used in other methods
        '''
        # old
        # self.stack.insert(0,number)
        # new
        self.stack.append(number)

    def _do_calc(self, operator):
        '''
        does the calculations and raises exception
        if there is insuffiecent operands
        '''
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        '''
        calls the adder class
        '''
        return self._do_calc(self.adder)

    def subtract(self):
        '''
        calls the subtracter class
        '''
        return self._do_calc(self.subtracter)

    def multiply(self):
        '''
        calls the multiplier class
        '''
        return self._do_calc(self.multiplier)

    def divide(self):
        '''
        calls the divider class
        '''
        return self._do_calc(self.divider)
