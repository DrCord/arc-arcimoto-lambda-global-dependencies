import unittest

from arcimoto.vehicle import Vehicle

from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestAllowsGovernor(unittest.TestCase, VehicleTestHelper):

    # test successes
    def test_allows_governor_success(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)

        try:
            result = VehicleObject.allows_governor
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIn(VehicleObject._query_firmware_version_for_vin_allows_governor, result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
