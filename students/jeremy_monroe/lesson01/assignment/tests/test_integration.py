""" Integration tests for inventory_management. """

import unittest
from unittest.mock import MagicMock, patch
import sys
import main

class InventoryIntegrationTest(unittest.TestCase):
    """ Integration test for inventory_management. """

    def test_integration_one(self):
        """
        Tests use of inventory_management module using simulated user input.
        """
        
        main.FULL_INVENTORY = {}

        inputs_list = ['1', 147, 'Chair', 1250, 'y', 'wood', 'l', '2', 147, 'q']
        user_inputs = (user_input for user_input in inputs_list)

        def mock_inputs(prompt):
            return next(user_inputs)

        with patch('builtins.input', mock_inputs):
            main.main_menu()()

        self.assertEqual('Chair', main.FULL_INVENTORY[147]['description'])

    def test_integration_two(self):
        """
        A second thorough use test of inventory_management.
        """
        
        main.FULL_INVENTORY = {}

        inputs_list = ['1', 765, 'Toaster', 300, 'n', 'y', 'Smeg', 110, '2', 765, 'q']
        user_inputs = (user_input for user_input in inputs_list)

        def mock_inputs(prompt):
            return next(user_inputs)

        with patch('builtins.input', mock_inputs):
            main.main_menu()()

        self.assertEqual('Smeg', main.FULL_INVENTORY[765]['brand'])