import unittest

from arcimoto.exceptions import ArcimotoException
import arcimoto.runtime
from arcimoto.user import (
    current,
    User
)

from tests._utility.unit_tests_user_credentials import UnitTestsUserCredentials


class TestCurrent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        arcimoto.runtime._event = None

    # test successes
    def test_current_success_token_in_event(self):
        UnitTestsUserCredentialsObject = UnitTestsUserCredentials()
        arcimoto.runtime._event = UnitTestsUserCredentialsObject.args_with_token
        try:
            result = current(mock=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, User)
        arcimoto.runtime._event = None

    def test_current_success_token_not_in_event(self):
        arcimoto.runtime._event = {}
        try:
            result = current(mock=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, User)
        arcimoto.runtime._event = None

    # test errors
    def test_current_error_event_not_set(self):
        with self.assertRaises(ArcimotoException):
            current(mock=True)


if __name__ == '__main__':
    unittest.main()
