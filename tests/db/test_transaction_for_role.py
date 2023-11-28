import unittest

from arcimoto.db import transaction_for_role
from arcimoto.exceptions import ArcimotoException


class TestTransactionForRole(unittest.TestCase):

    # test successes
    def test_transaction_for_role_success(self):
        @transaction_for_role
        def to_be_decorated(role_name):
            pass

        try:
            to_be_decorated('test-role')
        except Exception as e:
            self.fail(f'test failed: {e}')

    # test errors
    def test_transaction_for_role_error_function_raises_exception(self):
        @transaction_for_role
        def to_be_decorated(role_name):
            raise Exception('not successful')

        with self.assertRaises(Exception):
            to_be_decorated('test-role')()

    def test_transaction_for_role_error_input_role_name_null(self):
        @transaction_for_role
        def to_be_decorated(role_name):
            pass

        with self.assertRaises(ArcimotoException):
            to_be_decorated(None)()


if __name__ == '__main__':
    unittest.main()
