'''note'''
from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class AdderTests(TestCase):
    '''doc string'''
    def test_adding(self):
        '''doc string'''
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    '''doc string'''
    def test_subtracting(self):
        '''doc string'''
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    '''doc string'''
    def test_multipling(self):
        '''doc string'''
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    '''doc string'''
    def test_dividing(self):
        '''doc string'''
        divider = Divider()

        for i in range(-10, 10):
            for j in range(1, 10):
                self.assertEqual(i / j, divider.calc(i, j))


class CalculatorTests(TestCase):
    '''doc string'''
    def setUp(self):
        '''doc string'''
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter,
                                     self.multiplier, self.divider)

    def test_insufficient_operands(self):
        '''doc string'''
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        '''doc string'''
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(2, 1)

    def test_subtracter_call(self):
        '''doc string'''
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(2, 1)

    def test_multiplier_call(self):
        '''doc string'''
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(2, 1)

    def test_divider_call(self):
        '''doc string'''
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(2, 1)
