import unittest
import warnings

from arcimoto.note import ReplicateNotification


class TestReplicateNotification(unittest.TestCase):

    message = f'{__name__}_unit_test created'

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            'ignore',
            category=ResourceWarning
        )

    # test successes
    def test_replicate_notification_success(self):
        try:
            ReplicateNotification(self.message)
        except Exception as e:
            self.fail(f'test failed: {e}')


if __name__ == '__main__':
    unittest.main()
