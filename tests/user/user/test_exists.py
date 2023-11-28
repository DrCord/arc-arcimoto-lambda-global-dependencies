import unittest

from arcimoto.user import User


class TestExists(unittest.TestCase):

    # test successes
    def test_exists_success(self):
        UserObject = User(mock=True)
        self.assertFalse(UserObject.exists)
        UserObject.has_profile = True
        self.assertTrue(UserObject.exists)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
