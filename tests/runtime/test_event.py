import unittest

from arcimoto.exceptions import ArcimotoException
import arcimoto.runtime


class TestEvent(unittest.TestCase):

    # test successes
    def test_event_success(self):
        arcimoto.runtime._event = {}
        try:
            result = arcimoto.runtime.event()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(result, arcimoto.runtime._event)

    # test errors
    def test_event_error(self):
        arcimoto.runtime._event = None
        with self.assertRaises(ArcimotoException):
            arcimoto.runtime.event()


if __name__ == '__main__':
    unittest.main()
