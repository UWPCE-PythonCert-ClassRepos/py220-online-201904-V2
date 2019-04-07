""" Integration tests for inventory_management. """

import unittest
from unittest.mock import MagicMock, patch
import sys
import main

class InventoryIntegrationTest(unittest.TestCase):
    """ Integration test for inventory_management. """

    def test_integration_one(self):
        """ The main test. """
        
        main.FULL_INVENTORY = {}

        user_inputs = (user_input for user_input in ['1', 147, 'Chair', 1250, y, 'wood', 'l', '2', 147, 'q']

