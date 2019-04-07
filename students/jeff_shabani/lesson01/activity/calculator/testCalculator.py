#!/usr/bin/env python3

import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from adder import Adder
from subtracter import Subtracter
from divider import Divider
from multiplier import Multiplier
from calculator import Calculator
from exceptions import InsufficientOperands


class AdderTests(TestCase):

    def test_adding(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtractorTests(TestCase):

    def test_subtracting(self):
        subtractir = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtractir.calc(i, j))


class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtractor = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtractor, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(2)
        self.calculator.enter_number(1)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtractor_call(self):
        self.subtractor.calc = MagicMock(return_value=0)

        self.calculator.enter_number(2)
        self.calculator.enter_number(1)
        self.calculator.subtract()

        self.subtractor.calc.assert_called_with(1, 2)


class ModuleTests:

    def test_module(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(5)
        calculator.enter_number(2)

        calculator.multiply()

        calculator.enter_number(46)

        calculator.add()

        calculator.enter_number(8)

        calculator.divide()

        calculator.enter_number(1)

        result = calculator.subtract()

        self.assertEqual(0, result)


class MultiplierTests(TestCase):

    def test_multiplication(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(10)
        calculator.enter_number(12)

        result = calculator.multiply()
        self.assertEqual(120, result)
        del calculator

    @unittest.expectedFailure
    def test_multiplication_error(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(1)
        calculator.enter_number(12)

        result = calculator.multiply()
        self.assertEqual(120, result)
        del calculator


class DividerTests(TestCase):

    def test_division(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(2)
        calculator.enter_number(10)

        result = calculator.divide()
        self.assertEqual(5, result)
        del calculator

    @unittest.expectedFailure
    def test_division_error(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(24)
        calculator.enter_number(12)

        result = calculator.divide()
        self.assertEqual(3, result)
        del calculator

class SubtracterTests(TestCase):

    def test_subtraction(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(2)
        calculator.enter_number(10)

        result = calculator.subtract()
        self.assertEqual(8, result)
        del calculator

    @unittest.expectedFailure
    def test_subtraction_error(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(24)
        calculator.enter_number(12)

        result = calculator.subtract()
        self.assertEqual(12, result)
        del calculator

class AdditionTests(TestCase):

    def test_subtraction(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(-2)
        calculator.enter_number(10)

        result = calculator.add()
        self.assertEqual(8, result)
        del calculator