import unittest
import warnings

from arcimoto.db import transaction
from arcimoto.runtime import (
    _set_context,
    _set_role
)

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME
from tests._utility.mock.lambda_mock import AwsLambdaContextMock


class TestTransaction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_transaction_success_role_set(self):
        @transaction
        def to_be_decorated(**kwargs):
            pass

        context = AwsLambdaContextMock()
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)
        _set_context(context)

        try:
            result = to_be_decorated(mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    def test_transaction_success_role_unset(self):
        @transaction
        def to_be_decorated(**kwargs):
            pass

        context = AwsLambdaContextMock()
        # use known good existing lambda name for this test
        context.lambda_name = 'list_telemetry_vehicles'
        _set_context(context)

        try:
            result = to_be_decorated(mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)

    # test errors
    def test_transaction_error_function_raises_exception(self):
        @transaction
        def to_be_decorated():
            raise Exception('not successful')

        with self.assertRaises(Exception):
            to_be_decorated(mute=True)()


if __name__ == '__main__':
    unittest.main()
