import unittest

from arcimoto.exceptions import (
    ArcimotoException,
    ArcimotoHighAlertException,
    ArcimotoAlertException,
    ArcimotoFirmwareAlertException,
    ArcimotoManufacturingAlertException,
    ArcimotoNetworkAlertException,
    ArcimotoOrdersAlertException,
    ArcimotoREEFAlertException,
    ArcimotoReplicateAlertException,
    ArcimotoServiceAlertException,
    ArcimotoTelemetryAlertException,
    ArcimotoYRiskAlertException,
    ArcimotoPermissionError,
    ArcimotoArgumentError,
    ArcimotoNotFoundError,
    ArcimotoNoStepUnrollException
)


class TestExceptions(unittest.TestCase):

    msg = f'{__name__}_unit_test created'

    # test successes
    def test_exception_success_ArcimotoException(self):
        with self.assertRaises(ArcimotoException):
            raise ArcimotoException(self.msg)

    def test_exception_success_ArcimotoHighAlertException(self):
        with self.assertRaises(ArcimotoHighAlertException):
            raise ArcimotoHighAlertException(self.msg)

    def test_exception_success_ArcimotoAlertException(self):
        with self.assertRaises(ArcimotoAlertException):
            raise ArcimotoAlertException(self.msg)

    def test_exception_success_ArcimotoFirmwareAlertException(self):
        with self.assertRaises(ArcimotoFirmwareAlertException):
            raise ArcimotoFirmwareAlertException(self.msg)

    def test_exception_success_ArcimotoManufacturingAlertException(self):
        with self.assertRaises(ArcimotoManufacturingAlertException):
            raise ArcimotoManufacturingAlertException(self.msg)

    def test_exception_success_ArcimotoNetworkAlertException(self):
        with self.assertRaises(ArcimotoNetworkAlertException):
            raise ArcimotoNetworkAlertException(self.msg)

    def test_exception_success_ArcimotoOrdersAlertException(self):
        with self.assertRaises(ArcimotoOrdersAlertException):
            raise ArcimotoOrdersAlertException(self.msg)

    def test_exception_success_ArcimotoREEFAlertException(self):
        with self.assertRaises(ArcimotoREEFAlertException):
            raise ArcimotoREEFAlertException(self.msg)

    def test_exception_success_ArcimotoReplicateAlertException(self):
        with self.assertRaises(ArcimotoReplicateAlertException):
            raise ArcimotoReplicateAlertException(self.msg)

    def test_exception_success_ArcimotoServiceAlertException(self):
        with self.assertRaises(ArcimotoServiceAlertException):
            raise ArcimotoServiceAlertException(self.msg)

    def test_exception_success_ArcimotoTelemetryAlertException(self):
        with self.assertRaises(ArcimotoTelemetryAlertException):
            raise ArcimotoTelemetryAlertException(self.msg)

    def test_exception_success_ArcimotoYRiskAlertException(self):
        with self.assertRaises(ArcimotoYRiskAlertException):
            raise ArcimotoYRiskAlertException(self.msg)

    def test_exception_success_ArcimotoPermissionError(self):
        with self.assertRaises(ArcimotoPermissionError):
            raise ArcimotoPermissionError(self.msg)

    def test_exception_success_ArcimotoArgumentError(self):
        with self.assertRaises(ArcimotoArgumentError):
            raise ArcimotoArgumentError(self.msg)

    def test_exception_success_ArcimotoNotFoundError(self):
        with self.assertRaises(ArcimotoNotFoundError):
            raise ArcimotoNotFoundError(self.msg)

    def test_exception_success_ArcimotoNoStepUnrollException(self):
        with self.assertRaises(ArcimotoNoStepUnrollException):
            raise ArcimotoNoStepUnrollException(self.msg)


if __name__ == '__main__':
    unittest.main()
