import unittest

from arcimoto.user import User


class TestGetGroups(unittest.TestCase):

    # test successes
    def test_get_groups_success(self):
        UserObject = User(mock=True)
        try:
            UserObject.get_groups(mock=True)
        except Exception as e:
            self.fail(f'test failed {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
