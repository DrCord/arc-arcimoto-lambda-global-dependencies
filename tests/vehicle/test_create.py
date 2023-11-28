import unittest

from arcimoto.runtime import _set_role
from arcimoto.vehicle import Vehicle

from tests._utility.constants import (
    DEFAULT_TEST_LAMBDA_ROLE_NAME,
    DEFAULT_TEST_MODEL_RELEASE_ID
)
from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestCreate(unittest.TestCase, VehicleTestHelper):

    # test successes
    def test_create_success(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)

        try:
            result = VehicleObject.create(DEFAULT_TEST_MODEL_RELEASE_ID, mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(VehicleObject._query_vehicle_create, result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
