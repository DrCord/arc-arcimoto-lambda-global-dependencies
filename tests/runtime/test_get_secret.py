import unittest
import uuid
import warnings

from arcimoto.runtime import get_secret

from tests._utility.constants import DEFAULT_TEST_SECRET_NAME

from arcimoto_aws_services.secretsmanager import SecretsManagerService


class TestGetSecret(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_get_secret_success(self):
        try:
            result = get_secret(DEFAULT_TEST_SECRET_NAME)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, dict)

    # test errors
    def test_get_secret_error_secret_not_found(self):
        SecretsManagerServiceObject = SecretsManagerService()
        with self.assertRaises(SecretsManagerServiceObject.client.exceptions.ResourceNotFoundException):
            get_secret(f'{DEFAULT_TEST_SECRET_NAME}_{uuid.uuid4()}')


if __name__ == '__main__':
    unittest.main()
