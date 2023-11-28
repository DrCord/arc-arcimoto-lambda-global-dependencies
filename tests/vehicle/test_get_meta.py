import unittest

from arcimoto.vehicle import Vehicle

from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestGetMeta(unittest.TestCase, VehicleTestHelper):

    # test successes
    def test_get_meta_success(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)

        try:
            VehicleObject.get_meta('test_section', 'test_key')
        except Exception as e:
            self.fail(f'test failed: {e}')

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
