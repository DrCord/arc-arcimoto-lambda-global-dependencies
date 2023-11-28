import unittest

from arcimoto.runtime import (
    get_role,
    _set_role
)

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME


class TestGetRole(unittest.TestCase):

    # test successes
    def test_get_role_success_role_set(self):
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)
        try:
            result = get_role()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, str)

    def test_get_role_success_role_unset(self):
        _set_role(None)
        try:
            result = get_role()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
