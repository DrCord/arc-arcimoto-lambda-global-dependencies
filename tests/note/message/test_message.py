import unittest

from arcimoto.note import (
    _DEFAULT_SEVERITY,
    _DEFAULT_SOURCE,
    _DEFAULT_SOURCE_TYPE,
    Message
)


class TestMessage(unittest.TestCase):

    message = f'{__name__}_unit_test created'

    # test successes
    def test_message_success(self):
        try:
            Message(self.message, _DEFAULT_SOURCE_TYPE, _DEFAULT_SEVERITY, _DEFAULT_SOURCE, {}, None)
        except Exception as e:
            self.fail(f'test failed: {e}')


if __name__ == '__main__':
    unittest.main()
