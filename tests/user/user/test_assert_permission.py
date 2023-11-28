import unittest

from arcimoto.exceptions import ArcimotoPermissionError
from arcimoto.user import User

from tests._utility.constants import DEFAULT_TEST_PERMISSION_NAME


class TestAssertPermission(unittest.TestCase):

    # test successes
    def test_assert_permission_success(self):
        UserObject = User(mock=True)
        UserObject.roles = {
            DEFAULT_TEST_PERMISSION_NAME: '*'
        }

        try:
            UserObject.assert_permission(DEFAULT_TEST_PERMISSION_NAME, mute=True)
        except Exception as e:
            self.fail(f'test failed {e}')

    # test errors
    def test_assert_permission_error_unauthorized(self):
        UserObject = User(mock=True)

        with self.assertRaises(ArcimotoPermissionError):
            UserObject.assert_permission(DEFAULT_TEST_PERMISSION_NAME, mute=True)


if __name__ == '__main__':
    unittest.main()
