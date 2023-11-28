import unittest
import warnings

from arcimoto.db import close
from arcimoto.runtime import _set_role

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME


class TestClose(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_close_success_input_role(self):
        try:
            close(DEFAULT_TEST_LAMBDA_ROLE_NAME)
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_close_success_input_empty(self):
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)
        try:
            close()
        except Exception as e:
            self.fail(f'test failed: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
