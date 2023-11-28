import unittest

from arcimoto.tests import process_result_type
from tests.tests.helpers import TestsResult


class TestProcessResultType(unittest.TestCase):

    # test successes
    def test_process_result_type_success_input_skipped(self):
        TestsResultObject = TestsResult()
        TestsResultObject.skip_add()
        try:
            result = process_result_type(TestsResultObject.results.skipped, 'skipped').get('runTest', {})
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('status', None), 'failure')
        self.assertEqual(result.get('type', None), 'skipped')

    def test_process_result_type_success_input_failures(self):
        TestsResultObject = TestsResult()
        TestsResultObject.failure_add()
        try:
            result = process_result_type(TestsResultObject.results.failures, 'failure').get('runTest', {})
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('status', None), 'failure')
        self.assertEqual(result.get('type', None), 'failure')

    def test_process_result_type_success_input_errors(self):
        TestsResultObject = TestsResult()
        TestsResultObject.error_add()
        try:
            result = process_result_type(TestsResultObject.results.errors, 'error').get('runTest', {})
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('status', None), 'failure')
        self.assertEqual(result.get('type', None), 'error')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
