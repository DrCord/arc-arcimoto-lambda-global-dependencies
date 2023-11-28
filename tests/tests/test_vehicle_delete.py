
import unittest

from arcimoto.exceptions import ArcimotoException
from arcimoto.runtime import _set_role

from arcimoto.tests import (
    uuid_vin_get,
    vehicle_delete
)

from tests._utility.constants import (
    DEFAULT_TEST_LAMBDA_ROLE_NAME,
    VEHICLES_PUBLIC_LAMBDA_ROLE_NAME
)


class TestVehicleDelete(unittest.TestCase):

    # test successes
    # Unable to test success as requires being in VPC and specific security group to connect to RDS instance

    # test errors
    def test_vehicle_delete_error_no_role_set(self):
        with self.assertRaises(ArcimotoException):
            vehicle_delete(uuid_vin_get(), mute=True)

    def test_vehicle_delete_error_no_secret_found_for_role(self):
        _set_role(DEFAULT_TEST_LAMBDA_ROLE_NAME)
        with self.assertRaises(ArcimotoException):
            vehicle_delete(uuid_vin_get(), mute=True)

    def test_vehicle_delete_error_timeout(self):
        _set_role(VEHICLES_PUBLIC_LAMBDA_ROLE_NAME)
        with self.assertRaises(ArcimotoException):
            vehicle_delete(uuid_vin_get(), mute=True)


if __name__ == '__main__':
    unittest.main()
