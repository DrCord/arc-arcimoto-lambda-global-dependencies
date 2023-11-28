import unittest

from arcimoto.user import authenticated_cursor_request


class TestAuthenticatedCursorRequest(unittest.TestCase):

    # test successes
    def test_authenticated_cursor_request_success_no_input(self):
        try:
            result = authenticated_cursor_request(None, True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertTrue(result[1])

    def test_authenticated_cursor_request_success_input(self):
        try:
            result = authenticated_cursor_request({}, True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertFalse(result[1])

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
