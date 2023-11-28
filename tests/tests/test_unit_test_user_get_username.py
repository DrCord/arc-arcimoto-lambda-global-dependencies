import unittest

from arcimoto.tests import unit_test_user_get_username


class TestUnitTestUserGetUsername(unittest.TestCase):

    # test successes
    def test_unit_test_user_get_username_success_non_admin(self):
        try:
            result = unit_test_user_get_username()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, str)

    def test_unit_test_user_get_username_success_admin(self):
        try:
            result = unit_test_user_get_username(True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, str)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
