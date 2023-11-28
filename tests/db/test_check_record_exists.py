import unittest

from arcimoto.db import check_record_exists


class TestCheckRecordExists(unittest.TestCase):

    table_name = 'vehicle'
    test_record = {'vin': 'fake-VIN'}

    # test successes
    def test_check_record_exists_success_input_column_to_check_null(self):
        try:
            check_record_exists(self.table_name, self.test_record, None, True)
        except Exception as e:
            self.fail(f'test failed: {e}')

    def test_check_record_exists_success_input_column_to_check_set(self):
        try:
            check_record_exists(self.table_name, self.test_record, 'vin', True)
        except Exception as e:
            self.fail(f'test failed: {e}')


if __name__ == '__main__':
    unittest.main()
