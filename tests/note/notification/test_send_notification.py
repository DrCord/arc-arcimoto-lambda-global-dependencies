import unittest
import warnings

from arcimoto.note import (
    _DEFAULT_SEVERITY,
    _DEFAULT_SOURCE_TYPE,
    Notification,
    SEVERITY_CRITICAL,
    SEVERITY_INFO,
    SEVERITY_ERROR,
    SEVERITY_WARNING
)
from tests._utility.constants import DEFAULT_TEST_LAMBDA_NAME


class TestSendNotification(unittest.TestCase):

    message = f'{__name__}_unit_test created'

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_send_notification_success_input_message_only(self):
        try:
            Notification(self.message)
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_send_notification_success_input_severity_critical(self):
        try:
            Notification(
                self.message,
                _DEFAULT_SOURCE_TYPE,
                None,
                severity=SEVERITY_CRITICAL
            )
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_send_notification_success_input_severity_error(self):
        try:
            Notification(
                self.message,
                _DEFAULT_SOURCE_TYPE,
                None,
                severity=SEVERITY_ERROR
            )
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_send_notification_success_input_severity_info(self):
        try:
            Notification(
                self.message,
                _DEFAULT_SOURCE_TYPE,
                None,
                severity=SEVERITY_INFO
            )
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_send_notification_success_input_severity_warning(self):
        try:
            Notification(
                self.message,
                _DEFAULT_SOURCE_TYPE,
                None,
                severity=SEVERITY_WARNING
            )
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_send_notification_success_input_channel(self):
        try:
            Notification(
                self.message,
                _DEFAULT_SOURCE_TYPE,
                None,
                _DEFAULT_SEVERITY,
                {},
                'telemetry'
            )
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_send_notification_success_input_source(self):
        try:
            Notification(
                self.message,
                _DEFAULT_SOURCE_TYPE,
                DEFAULT_TEST_LAMBDA_NAME
            )
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_send_notification_success_input_source_type(self):
        try:
            Notification(
                self.message,
                'state_machine',
                'test-state-machine-name'
            )
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_send_notification_success_input_data(self):
        try:
            Notification(
                self.message,
                _DEFAULT_SOURCE_TYPE,
                None,
                _DEFAULT_SEVERITY,
                {'prop-test': 'test-value'}
            )
        except Exception as e:
            self.fail(f'test failed: {e}')


if __name__ == '__main__':
    unittest.main()
