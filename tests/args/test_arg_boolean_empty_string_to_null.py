import unittest

from arcimoto.args import arg_boolean_empty_string_to_null


class TestArgBooleanEmptyStringToNull(unittest.TestCase):

    # test successes
    def test_validate_success_input_empty_string(self):
        try:
            result = arg_boolean_empty_string_to_null('')
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    def test_validate_success_input_value_none(self):
        try:
            result = arg_boolean_empty_string_to_null('None')
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    def test_validate_success_input_value_falsy(self):
        try:
            result = arg_boolean_empty_string_to_null('False')
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertFalse(result)

    def test_validate_success_input_value_truthy(self):
        try:
            result = arg_boolean_empty_string_to_null('True')
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertTrue(result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
