import unittest

from arcimoto.runtime import get_function_name


class TestGetFunctionName(unittest.TestCase):

    # test successes
    def test_get_function_name_success(self):

        try:
            result = get_function_name()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, str)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
