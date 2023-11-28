import unittest

from arcimoto.user import User


class TestAuthenticated(unittest.TestCase):

    # test successes
    def test_authenticated_success(self):
        UserObject = User(mock=True)
        self.assertFalse(UserObject.authenticated)
        UserObject.username = 'mock_username'
        self.assertTrue(UserObject.authenticated)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
