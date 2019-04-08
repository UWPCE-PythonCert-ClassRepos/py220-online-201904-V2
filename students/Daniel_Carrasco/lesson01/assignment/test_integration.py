'''
module docstring
'''

from unittest import TestCase
from unittest.mock import patch


class ModuleTest(TestCase):
    '''
    class docstring
    '''

    test_dict = {
        'productcode': 'AB123',
        'description': 'TEST',
        'marketprice': '150.00',
        'rentalprice': '50.25',
                }

    @patch('inventory_management.main.addnewitem', return_value=test_dict)
    def test_main(self, addnewitem):
        '''
        method doc string
        '''

        dict_inv = {
            'productcode': 'AB123',
            'description': 'TEST',
            'marketprice': '150.00',
            'rentalprice': '50.25',
        }
        self.assertEqual(addnewitem(), dict_inv)
