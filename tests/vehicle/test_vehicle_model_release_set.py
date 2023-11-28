import unittest

from arcimoto.runtime import _set_role
from arcimoto.vehicle import Vehicle

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME
from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestVehicleModelReleaseSet(unittest.TestCase, VehicleTestHelper):

    VehicleObject = None

    @classmethod
    def setUpClass(cls):
        cls.VehicleObject = Vehicle(cls.vin, mock=True, mute=True)
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)

    # test successes
    def test_vehicle_model_release_set_success(self):
        try:
            self.VehicleObject.vehicle_model_release_set(1, mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
