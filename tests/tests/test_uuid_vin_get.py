import unittest

import arcimoto.runtime
from arcimoto.runtime import (
    ENV_DEV,
    ENV_PROD
)

from arcimoto.tests import uuid_vin_get


class TestUuidVinGet(unittest.TestCase):

    # test successes
    def test_uuid_vin_get_success_env_default(self):
        try:
            result = uuid_vin_get()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIn(f'{ENV_DEV.upper()}-TEST-VIN', result)

    def test_uuid_vin_get_success_env_prod(self):
        arcimoto.runtime._env = ENV_PROD
        try:
            result = uuid_vin_get()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIn('TEST-VIN', result)
        # reset arcimoto.runtime._env
        arcimoto.runtime._env = ENV_DEV

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
