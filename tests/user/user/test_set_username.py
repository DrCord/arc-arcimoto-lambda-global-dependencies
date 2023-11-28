import unittest
import uuid

from arcimoto.user import User


class TestSetUsername(unittest.TestCase):

    # test successes
    def test_set_username_success(self):
        UserObject = User(mock=True)
        username = f'unit-test_{uuid.uuid4}'
        self.assertFalse(UserObject.get_username())
        try:
            UserObject.set_username(username)
        except Exception as e:
            self.fail(f'test failed {e}')
        self.assertEqual(UserObject.get_username(), username)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
