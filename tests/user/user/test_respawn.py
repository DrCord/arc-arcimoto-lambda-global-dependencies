import unittest
import uuid

import arcimoto.runtime
from arcimoto.user import User


class TestRespawn(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        arcimoto.runtime._event = None

    # test successes
    def test_respawn_success(self):
        username = f'unit-test_{uuid.uuid4}'
        UserObject = User(mock=True)
        try:
            UserObject.respawn(username, mock=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(UserObject.get_username(), username)

    # # test errors
    # None


if __name__ == '__main__':
    unittest.main()
