import unittest

from arcimoto.args import arg_integer_empty_string_to_null


class TestArgIntegerEmptyStringToNull(unittest.TestCase):

    # test successes
    def test_arg_integer_empty_string_to_null_success_input_empty_string(self):
        try:
            result = arg_integer_empty_string_to_null('')
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    def test_arg_integer_empty_string_to_null_success_input_value_none(self):
        try:
            result = arg_integer_empty_string_to_null('None')
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    def test_arg_integer_empty_string_to_null_success_input_value_not_empty(self):
        value = '42'
        try:
            result = arg_integer_empty_string_to_null(value)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(result, int(value))

    # test errors
    def test_arg_integer_empty_string_to_null_error_invalid_literal_for_int_with_base_10(self):
        value = 'not a number value'
        with self.assertRaises(ValueError):
            arg_integer_empty_string_to_null(value)


if __name__ == '__main__':
    unittest.main()
