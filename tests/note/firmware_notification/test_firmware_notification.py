import unittest
import warnings

from arcimoto.note import FirmwareNotification


class TestFirmwareNotification(unittest.TestCase):

    message = f'{__name__}_unit_test created'

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_firmware_notification_success(self):
        try:
            FirmwareNotification(self.message)
        except Exception as e:
            self.fail(f'test failed: {e}')


if __name__ == '__main__':
    unittest.main()
