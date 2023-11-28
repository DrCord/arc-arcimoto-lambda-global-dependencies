import unittest

from arcimoto.vehicle import Vehicle

from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestExists(unittest.TestCase, VehicleTestHelper):

    # test successes
    def test_exists_success(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)

        try:
            result = VehicleObject.exists
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(VehicleObject._query_vehicle_exists, result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
