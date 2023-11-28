import unittest

from arcimoto.vehicle import Vehicle

from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestPinGenerate(unittest.TestCase, VehicleTestHelper):

    disallowed_pins = [
        '000000',
        '111111',
        '222222',
        '333333',
        '444444',
        '555555',
        '666666',
        '777777',
        '888888',
        '999999',
        '012345',
        '123456',
        '234567',
        '345678',
        '456789',
        '567890',
        '098765',
        '987654',
        '876543',
        '765432',
        '654321',
        '543210'
    ]

    # test successes
    def test_pin_generate_success(self):
        VehicleObject = Vehicle(self.vin, mock=True, mute=True)

        try:
            result = VehicleObject.pin_generate()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) == 6)
        self.assertNotIn(result, self.disallowed_pins)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
