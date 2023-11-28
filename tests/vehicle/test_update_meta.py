import unittest

from arcimoto.exceptions import ArcimotoArgumentError
from arcimoto.runtime import _set_role
from arcimoto.vehicle import Vehicle

from tests._utility.constants import DEFAULT_TEST_LAMBDA_ROLE_NAME
from tests.vehicle.vehicle_helper import VehicleTestHelper


class TestUpdateMeta(unittest.TestCase, VehicleTestHelper):

    reserved_meta_sections = ['vin', 'groups', 'telemetry']

    VehicleObject = None

    @classmethod
    def setUpClass(cls):
        cls.VehicleObject = Vehicle(cls.vin, mock=True, mute=True)
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)

    # test successes
    def test_update_meta_success(self):
        try:
            self.VehicleObject.update_meta('test-section', 'test-key', 'test-value', mute=True)
        except Exception as e:
            self.fail(f'test failed: {e}')

    # test errors
    def test_update_meta_error_section_in_reserved_sections(self):
        for reserved_meta_section in self.reserved_meta_sections:
            with self.assertRaises(ArcimotoArgumentError):
                self.VehicleObject.update_meta(reserved_meta_section, 'test-key', 'test-value', mute=True)


if __name__ == '__main__':
    unittest.main()
