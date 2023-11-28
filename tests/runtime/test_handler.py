import unittest
import warnings

from arcimoto.exceptions import (
    ArcimotoAlertException,
    ArcimotoArgumentError,
    ArcimotoFirmwareAlertException,
    ArcimotoHighAlertException,
    ArcimotoManufacturingAlertException,
    ArcimotoNetworkAlertException,
    ArcimotoOrdersAlertException,
    ArcimotoREEFAlertException,
    ArcimotoReplicateAlertException,
    ArcimotoServiceAlertException,
    ArcimotoTelemetryAlertException,
    ArcimotoYRiskAlertException
)

from arcimoto.runtime import (
    handler,
    _set_role
)

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME
from tests._utility.mock.lambda_mock import AwsLambdaContextMock


class TestHandler(unittest.TestCase):

    context = AwsLambdaContextMock()
    event = {}
    msg = 'not successful'

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)

    # test successes
    def test_handler_success_role_set(self):
        @handler
        def to_be_decorated(**kwargs):
            pass

        try:
            result = to_be_decorated(self.event, self.context)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)

    def test_handler_success_role_unset(self):
        @handler
        def to_be_decorated(**kwargs):
            pass

        context = AwsLambdaContextMock()
        # use known good existing lambda name for this test
        context.lambda_name = 'list_telemetry_vehicles'

        try:
            result = to_be_decorated(self.event, context)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)

    # test errors
    def test_handler_error_function_raises_ArcimotoAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoAlertException(self.msg)

        with self.assertRaises(ArcimotoAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoArgumentError(self):
        @handler
        def to_be_decorated():
            raise ArcimotoArgumentError(self.msg)

        with self.assertRaises(ArcimotoArgumentError):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoFirmwareAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoFirmwareAlertException(self.msg)

        with self.assertRaises(ArcimotoFirmwareAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoHighAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoHighAlertException(self.msg)

        with self.assertRaises(ArcimotoHighAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoManufacturingAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoManufacturingAlertException(self.msg)

        with self.assertRaises(ArcimotoManufacturingAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoNetworkAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoNetworkAlertException(self.msg)

        with self.assertRaises(ArcimotoNetworkAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoOrdersAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoOrdersAlertException(self.msg)

        with self.assertRaises(ArcimotoOrdersAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoREEFAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoREEFAlertException(self.msg)

        with self.assertRaises(ArcimotoREEFAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoReplicateAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoReplicateAlertException(self.msg)

        with self.assertRaises(ArcimotoReplicateAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoServiceAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoServiceAlertException(self.msg)

        with self.assertRaises(ArcimotoServiceAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoTelemetryAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoTelemetryAlertException(self.msg)

        with self.assertRaises(ArcimotoTelemetryAlertException):
            to_be_decorated(self.event, self.context)()

    def test_handler_error_function_raises_ArcimotoYRiskAlertException(self):
        @handler
        def to_be_decorated():
            raise ArcimotoYRiskAlertException(self.msg)

        with self.assertRaises(ArcimotoYRiskAlertException):
            to_be_decorated(self.event, self.context)()


if __name__ == '__main__':
    unittest.main()
