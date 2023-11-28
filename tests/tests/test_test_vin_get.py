import unittest

import arcimoto.runtime
from arcimoto.runtime import (
    ENV_DEV,
    ENV_PROD
)

from arcimoto.tests import test_vin_get


class TestTestVinGet(unittest.TestCase):

    # test successes
    def test_test_vin_get_success_env_default(self):
        try:
            result = test_vin_get()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(result, f'{ENV_DEV.upper()}-TEST-VIN')

    def test_test_vin_get_success_env_prod(self):
        arcimoto.runtime._env = ENV_PROD
        try:
            result = test_vin_get()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(result, 'TEST-VIN')
        # reset arcimoto.runtime._env
        arcimoto.runtime._env = ENV_DEV

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
