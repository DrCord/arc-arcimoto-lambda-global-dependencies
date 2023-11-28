import unittest

from arcimoto.tests import handle_test_result
from tests.tests.helpers import TestsResult


class TestHandleTestResult(unittest.TestCase):

    # test successes
    def test_handle_test_result_success_no_tests_run_SUCCESS(self):
        TestsResultObject = TestsResult()
        try:
            result = handle_test_result(TestsResultObject.results)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)
        self.assertIn('SUCCESS', result.get('status', ''))

    def test_handle_test_result_success_tests_run_SUCCESS(self):
        # this test causes an extra 'dot' in the test runner output due to manually adding a successful test
        TestsResultObject = TestsResult()
        TestsResultObject.success_add()
        try:
            result = handle_test_result(TestsResultObject.results)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)
        self.assertIn('SUCCESS', result.get('status', ''))

    def test_handle_test_result_success_tests_run_FAILURE(self):
        TestsResultObject = TestsResult()
        TestsResultObject.failure_add()
        try:
            result = handle_test_result(TestsResultObject.results)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)
        self.assertIn('FAILURE', result.get('status', ''))

    def test_handle_test_result_success_tests_run_ERROR(self):
        TestsResultObject = TestsResult()
        TestsResultObject.failure_add()
        try:
            result = handle_test_result(TestsResultObject.results)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)
        self.assertIn('FAILURE', result.get('status', ''))

    def test_handle_test_result_success_tests_run_SKIP(self):
        TestsResultObject = TestsResult()
        TestsResultObject.skip_add()
        try:
            result = handle_test_result(TestsResultObject.results)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)
        self.assertIn('SUCCESS', result.get('status', ''))

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
