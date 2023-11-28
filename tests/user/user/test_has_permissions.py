import unittest

from arcimoto.user import User

from tests._utility.constants import DEFAULT_TEST_PERMISSION_NAME


class TestHasPermissions(unittest.TestCase):

    # test successes
    def test_has_permissions_success_user_has_permissions(self):
        UserObject = User(mock=True)
        UserObject.roles = {
            DEFAULT_TEST_PERMISSION_NAME: '*',
            f'{DEFAULT_TEST_PERMISSION_NAME}_2': '*'
        }

        try:
            result = UserObject.has_permissions([
                DEFAULT_TEST_PERMISSION_NAME,
                f'{DEFAULT_TEST_PERMISSION_NAME}_2'
            ])
        except Exception as e:
            self.fail(f'test failed {e}')
        self.assertTrue(result)

    def test_has_permissions_success_user_does_not_have_permissions(self):
        UserObject = User(mock=True)

        try:
            result = UserObject.has_permissions([DEFAULT_TEST_PERMISSION_NAME])
        except Exception as e:
            self.fail(f'test failed {e}')
        self.assertFalse(result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
