import unittest

from arcimoto.runtime import _set_role
from arcimoto.vehicle import Vehicle

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME
from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestManagedSessionStart(unittest.TestCase, VehicleTestHelper):

    # test successes
    def test_managed_session_start_success_input_pin_null(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)

        try:
            VehicleObject.managed_session_start('unit-test-user', None, None, mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_managed_session_start_success_input_pin_supplied(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)

        try:
            VehicleObject.managed_session_start('unit-test-user', None, '123456', mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
