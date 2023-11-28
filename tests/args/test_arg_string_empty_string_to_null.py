import unittest

from arcimoto.args import arg_string_empty_string_to_null


class TestArgStringEmptyStringToNull(unittest.TestCase):

    # test successes
    def test_arg_string_empty_string_to_null_success_input_empty_string(self):
        try:
            result = arg_string_empty_string_to_null('')
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    def test_arg_string_empty_string_to_null_success_input_value_none(self):
        try:
            result = arg_string_empty_string_to_null('None')
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    def test_arg_string_empty_string_to_null_success_input_value_not_empty(self):
        value = 'not a null value'
        try:
            result = arg_string_empty_string_to_null(value)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(result, value)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
