"""
calculator class
"""

from exceptions import InsufficientOperands


class Calculator(object):
    """
    main class
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        method to enter a number into the calculator
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        method for running a calculation
        """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        addition method
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        subtraction method
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        multiplication method
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        division method
        """
        return self._do_calc(self.divider)
