import unittest

from arcimoto.runtime import _set_role
from arcimoto.vehicle import Vehicle

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME
from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestManagedSessionMode(unittest.TestCase, VehicleTestHelper):

    # test successes
    def test_managed_session_mode_success(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)

        try:
            result = VehicleObject.managed_session_mode
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertFalse(result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
