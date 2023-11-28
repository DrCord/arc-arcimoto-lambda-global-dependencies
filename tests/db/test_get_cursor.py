import unittest
import warnings

from arcimoto.db import get_cursor
from arcimoto.exceptions import ArcimotoException
from arcimoto.runtime import _set_role

from tests._utility.constants import (
    DEFAULT_TEST_LAMBDA_ROLE_NAME,
    VEHICLES_PUBLIC_LAMBDA_ROLE_NAME
)


class TestGetCursor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_get_cursor_success_input_role(self):
        try:
            result = get_cursor(VEHICLES_PUBLIC_LAMBDA_ROLE_NAME, True)
        except Exception as e:
            self.fail(f'test failed: {e}')

        self.check_connection_string(result)

    def test_get_cursor_success_input_empty(self):
        _set_role(VEHICLES_PUBLIC_LAMBDA_ROLE_NAME)
        try:
            result = get_cursor(None, True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.check_connection_string(result)

    # test errors
    def test_get_cursor_error_secret_for_role_not_found(self):
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)
        with self.assertRaises(ArcimotoException):
            get_cursor(None, True)

    # test helpers (non-tests)
    def check_connection_string(self, result):
        # check if conn string was assembled correctly
        # dbname
        self.assertIn('dbname', result)
        self.assertIn('telemetryam', result)
        # user
        self.assertIn('user', result)
        self.assertIn('telwrite', result)
        # host
        self.assertIn('host', result)
        self.assertIn('tel-main-db-dev-auroradbcluster', result)
        # password
        self.assertIn('password', result)


if __name__ == '__main__':
    unittest.main()
