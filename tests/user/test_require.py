import unittest

from arcimoto.exceptions import ArcimotoPermissionError
import arcimoto.runtime
import arcimoto.user
from arcimoto.user import require

from tests._utility.constants import DEFAULT_TEST_PERMISSION_NAME


class TestRequire(unittest.TestCase):

    UserObject = None

    @classmethod
    def setUpClass(cls):
        arcimoto.runtime._current = None
        arcimoto.runtime._event = None

    # test successes
    def test_require_success(self):
        @require(DEFAULT_TEST_PERMISSION_NAME)
        def to_be_decorated(**kwargs):
            pass

        arcimoto.runtime._event = {}
        arcimoto.user.current(mock=True)
        arcimoto.user._current.roles = {
            DEFAULT_TEST_PERMISSION_NAME: '*'
        }
        try:
            result = to_be_decorated(mute=True, mock=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)
        arcimoto.runtime._current = None
        arcimoto.runtime._event = None

    # test errors
    def test_require_error_unauthorized_no_user(self):
        @require(DEFAULT_TEST_PERMISSION_NAME)
        def to_be_decorated(**kwargs):
            pass

        arcimoto.runtime._event = {}
        with self.assertRaises(ArcimotoPermissionError):
            to_be_decorated(mute=True, mock=True)
        arcimoto.runtime._current = None
        arcimoto.runtime._event = None

    def test_require_error_unauthorized_user_no_permissions(self):
        @require(DEFAULT_TEST_PERMISSION_NAME)
        def to_be_decorated(**kwargs):
            pass

        arcimoto.runtime._event = {}
        arcimoto.user.current(mock=True)
        with self.assertRaises(ArcimotoPermissionError):
            to_be_decorated(mute=True, mock=True)
        arcimoto.runtime._current = None
        arcimoto.runtime._event = None


if __name__ == '__main__':
    unittest.main()
