import uuid

from tests._utility.constants import (
    DEFAULT_AWS_ACCOUNT_ID,
    DEFAULT_AWS_REGION,
    DEFAULT_TEST_LAMBDA_NAME,
    DEV_ALIAS
)
from arcimoto_aws_services.lambda_service import LambdaService


class AwsLambdaContextMock:

    _lambda_name = None
    _invoked_function_arn = None
    _LambdaServiceObject = None

    def __init__(self, lambda_name=DEFAULT_TEST_LAMBDA_NAME, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lambda_name = lambda_name

    @property
    def invoked_function_arn(self):
        if self._invoked_function_arn is None:
            self._invoked_function_arn = self.LambdaServiceObject.lambda_arn_build(
                DEFAULT_AWS_REGION,
                DEFAULT_AWS_ACCOUNT_ID,
                self.lambda_name,
                DEV_ALIAS
            )
        return self._invoked_function_arn

    @property
    def function_name(self):
        return self._lambda_name

    @property
    def lambda_name(self):
        return self._lambda_name

    @lambda_name.setter
    def lambda_name(self, value):
        self._lambda_name_set(value)

    @property
    def LambdaServiceObject(self):
        if self._LambdaServiceObject is None:
            self._LambdaServiceObject = LambdaService()
        return self._LambdaServiceObject

    def _lambda_name_set(self, lambda_name=DEFAULT_TEST_LAMBDA_NAME):
        self._lambda_name = lambda_name
        if lambda_name == DEFAULT_TEST_LAMBDA_NAME:
            self._lambda_name += f'_{str(uuid.uuid4())}'
