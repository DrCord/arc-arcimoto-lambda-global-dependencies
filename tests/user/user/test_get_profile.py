import unittest

from arcimoto.user import User


class TestGetProfile(unittest.TestCase):

    # test successes
    def test_get_profile_success(self):
        UserObject = User(mock=True)
        try:
            UserObject.get_profile()
        except Exception as e:
            self.fail(f'test failed {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
