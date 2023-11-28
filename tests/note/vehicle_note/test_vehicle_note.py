import unittest
import warnings

from arcimoto.note import VehicleNote

from arcimoto.tests import test_vin_get


class TestVehicleNote(unittest.TestCase):

    message = f'{__name__}_unit_test created'

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_vehicle_note_success(self):
        try:
            VehicleNote(
                test_vin_get(),
                self.message
            )
        except Exception as e:
            self.fail(f'test failed: {e}')


if __name__ == '__main__':
    unittest.main()
