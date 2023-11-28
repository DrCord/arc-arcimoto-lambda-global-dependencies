import unittest

from arcimoto.runtime import _set_role
from arcimoto.vehicle import (
    ARCIMOTO_GROUP_ID,
    Vehicle
)

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME
from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestAddToGroup(unittest.TestCase, VehicleTestHelper):

    # test successes
    def test_add_to_group_success(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)

        try:
            result = VehicleObject.add_to_group(ARCIMOTO_GROUP_ID, mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIn(VehicleObject._query_vehicle_group_id_add_vin, result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
