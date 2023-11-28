from copy import deepcopy
import unittest

from arcimoto.exceptions import (
    ArcimotoAlertException,
    ArcimotoArgumentError,
    ArcimotoException,
    ArcimotoHighAlertException,
    ArcimotoNoStepUnrollException,
    ArcimotoNotFoundError,
    ArcimotoPermissionError
)
from arcimoto.runtime import boto_lambda_exception_handle


class TestBotoLambdaExceptionHandle(unittest.TestCase):

    payload = {
        'errorType': None,
        'errorMessage': 'unit test error message',
    }

    # test successes
    # None

    # test errors
    def test_boto_lambda_exception_handle_error_ArcimotoAlertException(self):
        payload = deepcopy(self.payload)
        payload['errorType'] = 'ArcimotoAlertException'
        with self.assertRaises(ArcimotoAlertException):
            boto_lambda_exception_handle(payload)

    def test_boto_lambda_exception_handle_error_ArcimotoArgumentError(self):
        payload = deepcopy(self.payload)
        payload['errorType'] = 'ArcimotoArgumentError'
        with self.assertRaises(ArcimotoArgumentError):
            boto_lambda_exception_handle(payload)

    def test_boto_lambda_exception_handle_error_ArcimotoHighAlertException(self):
        payload = deepcopy(self.payload)
        payload['errorType'] = 'ArcimotoHighAlertException'
        with self.assertRaises(ArcimotoHighAlertException):
            boto_lambda_exception_handle(payload)

    def test_boto_lambda_exception_handle_error_ArcimotoNoStepUnrollException(self):
        payload = deepcopy(self.payload)
        payload['errorType'] = 'ArcimotoNoStepUnrollException'
        with self.assertRaises(ArcimotoNoStepUnrollException):
            boto_lambda_exception_handle(payload)

    def test_boto_lambda_exception_handle_error_ArcimotoNotFoundError(self):
        payload = deepcopy(self.payload)
        payload['errorType'] = 'ArcimotoNotFoundError'
        with self.assertRaises(ArcimotoNotFoundError):
            boto_lambda_exception_handle(payload)

    def test_boto_lambda_exception_handle_error_ArcimotoPermissionError(self):
        payload = deepcopy(self.payload)
        payload['errorType'] = 'ArcimotoPermissionError'
        with self.assertRaises(ArcimotoPermissionError):
            boto_lambda_exception_handle(payload)

    def test_boto_lambda_exception_handle_error_ArcimotoException(self):
        with self.assertRaises(ArcimotoException):
            boto_lambda_exception_handle(self.payload)


if __name__ == '__main__':
    unittest.main()
