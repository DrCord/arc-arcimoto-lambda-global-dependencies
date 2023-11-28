import unittest

from arcimoto.user import User

from tests._utility.constants import DEFAULT_TEST_PERMISSION_NAME


class TestHasPermission(unittest.TestCase):

    # test successes
    def test_has_permission_success_user_has_permission(self):
        UserObject = User(mock=True)
        UserObject.roles = {
            DEFAULT_TEST_PERMISSION_NAME: '*'
        }

        try:
            result = UserObject.has_permission(DEFAULT_TEST_PERMISSION_NAME)
        except Exception as e:
            self.fail(f'test failed {e}')
        self.assertTrue(result)

    def test_has_permission_success_user_does_not_have_permission(self):
        UserObject = User(mock=True)

        try:
            result = UserObject.has_permission(DEFAULT_TEST_PERMISSION_NAME)
        except Exception as e:
            self.fail(f'test failed {e}')
        self.assertFalse(result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
