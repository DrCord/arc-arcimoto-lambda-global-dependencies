import unittest
import uuid
import warnings

from arcimoto.exceptions import ArcimotoException
import arcimoto.runtime

from arcimoto_aws_services.lambda_service import LambdaService

from tests._utility.constants import DEFAULT_TEST_LAMBDA_NAME

from tests._utility.unit_tests_user_credentials import UnitTestsUserCredentials


class TestInvokeLambda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_invoke_lambda_success_exists_and_no_authorization_required(self):
        arcimoto.runtime._event = {}
        arcimoto.runtime._env = arcimoto.runtime.ENV_DEV
        try:
            result = arcimoto.runtime.invoke_lambda(DEFAULT_TEST_LAMBDA_NAME, {}, mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)

    def test_invoke_lambda_success_exists_and_authorization_required(self):
        arcimoto.runtime._event = {}
        arcimoto.runtime._env = arcimoto.runtime.ENV_DEV
        UnitTestsUserCredentialsObject = UnitTestsUserCredentials()
        try:
            result = arcimoto.runtime.invoke_lambda(
                'list_telemetry_vehicles',
                UnitTestsUserCredentialsObject.args_with_token_admin,
                mute=True
            )
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)

    # NOTE
    # could be expanded to check each error type that can be returned
    # but would need the global dependencies layer attached to the test lambda
    # is it worthwhile?

    # test errors
    def test_invoke_lambda_error_event_access_outside_invocation(self):
        arcimoto.runtime._event = None
        arcimoto.runtime._env = arcimoto.runtime.ENV_DEV
        with self.assertRaises(ArcimotoException):
            arcimoto.runtime.invoke_lambda(DEFAULT_TEST_LAMBDA_NAME, {}, mute=True)

    def test_invoke_lambda_error_lambda_not_found(self):
        arcimoto.runtime._event = {}
        arcimoto.runtime._env = arcimoto.runtime.ENV_DEV
        LambdaServiceObject = LambdaService()
        with self.assertRaises(LambdaServiceObject.client.exceptions.ResourceNotFoundException):
            arcimoto.runtime.invoke_lambda(f'{DEFAULT_TEST_LAMBDA_NAME}_{uuid.uuid4()}', {}, mute=True)

    def test_invoke_lambda_error_env_not_found(self):
        arcimoto.runtime._event = {}
        arcimoto.runtime._env = f'{arcimoto.runtime._env}_{uuid.uuid4()}'
        LambdaServiceObject = LambdaService()
        with self.assertRaises(LambdaServiceObject.client.exceptions.ResourceNotFoundException):
            arcimoto.runtime.invoke_lambda(DEFAULT_TEST_LAMBDA_NAME, {}, mute=True)

    def test_invoke_lambda_error_unauthorized_no_user(self):
        arcimoto.runtime._event = {}
        arcimoto.runtime._env = arcimoto.runtime.ENV_DEV
        with self.assertRaises(Exception) as cm:
            arcimoto.runtime.invoke_lambda('list_telemetry_vehicles', {}, mute=True)
        self.assertEqual(str(cm.exception), 'Unauthorized')

    def test_invoke_lambda_error_unauthorized_with_user(self):
        arcimoto.runtime._event = {}
        arcimoto.runtime._env = arcimoto.runtime.ENV_DEV
        UnitTestsUserCredentialsObject = UnitTestsUserCredentials()
        with self.assertRaises(Exception) as cm:
            arcimoto.runtime.invoke_lambda(
                'list_telemetry_vehicles',
                UnitTestsUserCredentialsObject.args_with_token,
                mute=True
            )
        self.assertEqual(str(cm.exception), 'Unauthorized')


if __name__ == '__main__':
    unittest.main()
