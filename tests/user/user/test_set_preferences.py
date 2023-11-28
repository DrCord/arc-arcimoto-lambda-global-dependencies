import unittest

from arcimoto.user import User


class TestSetPreferences(unittest.TestCase):

    # test successes
    def test_set_preferences_success(self):
        UserObject = User(mock=True)
        try:
            result = UserObject.set_preferences(mock=True)
        except Exception as e:
            self.fail(f'test failed {e}')
        self.assertIsInstance(result, str)
        self.assertIn('SELECT', result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
