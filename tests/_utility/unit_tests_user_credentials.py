from arcimoto_aws_services.secretsmanager import SecretsManagerService

from tests._utility.constants import DEFAULT_TEST_SECRET_NAME


class UnitTestsUserCredentials(SecretsManagerService):

    unit_test_users_secret = None

    get_admin_user = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def args_with_token(self):
        if self.unit_test_users_secret is None:
            self.unit_test_users_secret_get()
        return {
            'params': {
                'header': {
                    'Authorization': self.token
                }
            }
        }

    @property
    def args_with_token_admin(self):
        if self.unit_test_users_secret is None:
            self.unit_test_users_secret_get()
        return {
            'params': {
                'header': {
                    'Authorization': self.token_admin
                }
            }
        }

    @property
    def token(self):
        if self.unit_test_users_secret is None:
            self.unit_test_users_secret_get()
        return self.unit_test_users_secret.get('USER_TOKEN_NON_ADMIN')

    @property
    def token_admin(self):
        if self.unit_test_users_secret is None:
            self.unit_test_users_secret_get()
        return self.unit_test_users_secret.get('USER_TOKEN_ADMIN')

    def unit_test_users_secret_get(self):
        self.unit_test_users_secret = self.get_secret(DEFAULT_TEST_SECRET_NAME)
