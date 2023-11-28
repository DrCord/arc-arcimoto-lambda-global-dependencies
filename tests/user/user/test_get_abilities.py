import unittest

from arcimoto.user import User


class TestGetAbilities(unittest.TestCase):

    # test successes
    def test_get_abilities_success(self):
        UserObject = User(mock=True)
        try:
            UserObject.get_abilities(mock=True)
        except Exception as e:
            self.fail(f'test failed {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
