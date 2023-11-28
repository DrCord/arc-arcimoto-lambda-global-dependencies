import datetime
import unittest

from arcimoto.db import datetime_record_output


class TestDatetimeRecordOutput(unittest.TestCase):

    datetime_object = datetime.datetime.now()

    # test successes
    def test_datetime_record_output_success_dateime_not_null(self):
        try:
            result = datetime_record_output(self.datetime_object)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, str)

    def test_datetime_record_output_success_datetime_null(self):
        try:
            result = datetime_record_output(None)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
