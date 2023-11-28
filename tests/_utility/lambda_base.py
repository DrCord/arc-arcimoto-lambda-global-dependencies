import uuid

from tests._utility.constants import DEFAULT_TEST_LAMBDA_NAME


class LambdaBase:

    _lambda_name = None

    def __init__(self, lambda_name=DEFAULT_TEST_LAMBDA_NAME, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lambda_name = lambda_name

    @property
    def lambda_name(self):
        return self._lambda_name

    @lambda_name.setter
    def lambda_name(self, value):
        self._lambda_name_set(value)

    def _lambda_name_set(self, lambda_name=DEFAULT_TEST_LAMBDA_NAME):
        self._lambda_name = lambda_name
        if lambda_name == DEFAULT_TEST_LAMBDA_NAME:
            self._lambda_name += f'_{str(uuid.uuid4())}'
