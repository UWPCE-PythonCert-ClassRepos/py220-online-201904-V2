#!/usr/bin/env python3

from io import StringIO
import unittest
from src.locke_manager import Locke
from unittest.mock import patch


class PerformanceTesting(unittest.TestCase):

    def test_small_boat_pass(self):
        """
        Test small boat and small locke. Boat size is less than
        locke capacity.
        """
        expected = f'Stopping the pumps\nOpening the doors\nClosing the doors' \
            f'\nRestarting the pumps'
        small_locke = Locke(7)
        klein_boat = 3
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            small_locke.move_boats_through(klein_boat, 'boatie')
            self.assertEqual(mocked_output.getvalue().strip(), expected)

        del small_locke
        del klein_boat

    def test_small_boat_bigger_than_locke(self):
        """
        Test small boat and small locke. Boat size is less than
        locke capacity.
        """
        expected = f'Boat boatie 8 exceeds capacity 7'
        small_locke = Locke(7)
        klein_boat = 8
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            small_locke.move_boats_through(klein_boat, 'boatie')
            self.assertEqual(mocked_output.getvalue().strip(), expected)

        del small_locke
        del klein_boat

    @unittest.expectedFailure
    def test_small_boat_failure(self):
        """
        Test small boat and small locke. Boat size is less than
        locke capacity.
        """
        expected = f'Stopping the pumps\nOpening the doors\nClosing the doors' \
            f'\nRestarting the pumps'
        small_locke = Locke(7)
        klein_boat = 10
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            small_locke.move_boats_through(klein_boat, 'boatie')
            self.assertEqual(mocked_output.getvalue().strip(), expected)

        del small_locke
        del klein_boat

    def test_big_boat_pass(self):
        """
        Test big boat and big locke. Boat size is less than
        locke capacity.
        """
        expected = f'Stopping the pumps\nOpening the doors\nClosing the doors' \
            f'\nRestarting the pumps'
        big_locke = Locke(7)
        klein_boat = 3
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            big_locke.move_boats_through(klein_boat, 'big boatie')
            self.assertEqual(mocked_output.getvalue().strip(), expected)

        del big_locke
        del klein_boat

    def test_big_boat_bigger_than_locke(self):
        """
        Test big boat and big locke. Boat size is less than
        locke capacity.
        """
        expected = f'Boat big boatie 8 exceeds capacity 7'
        big_locke = Locke(7)
        klein_boat = 8
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            big_locke.move_boats_through(klein_boat, 'big boatie')
            self.assertEqual(mocked_output.getvalue().strip(), expected)

        del big_locke
        del klein_boat

    @unittest.expectedFailure
    def test_big_boat_failure(self):
        """
        Test big boat and big locke. Boat size is less than
        locke capacity.
        """
        expected = f'Stopping the pumps\nOpening the doors\nClosing the doors' \
            f'\nRestarting the pumps'
        big_locke = Locke(7)
        klein_boat = 10
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            big_locke.move_boats_through(klein_boat, 'big boatie')
            self.assertEqual(mocked_output.getvalue().strip(), expected)

        del big_locke
        del klein_boat


if __name__ == '__main__':
    unittest.main()
