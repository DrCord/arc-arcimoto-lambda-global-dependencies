import datetime
import unittest

from arcimoto.db import prepare_update_query_and_params


class TestPrepareUpdateQueryAndParams(unittest.TestCase):

    datetime_object = datetime.datetime.now()
    table_name = 'recalls'
    where_predicates = [
        {
            'column': 'id',
            'operator': '=',
            'value': 1
        }
    ]
    columns_data = [
        {'mfr_campaign_id': 1},
        {'country': 'US'},
        {'title': 'test'},
        {'description': 'test'},
        {'nhtsa_number': 'test'},
        {'date': datetime_object},
        {'remedy_id': 1},
        {'safety_recall': True},
        {'safety_description': 'test'},
        {'status': 'active'}
    ]

    # test successes
    def test_prepare_update_query_and_params_success_input_allow_none_false(self):
        try:
            result = prepare_update_query_and_params(
                self.table_name,
                self.where_predicates,
                self.columns_data
            )
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, tuple)

    def test_prepare_update_query_and_params_success_input_allow_none_true(self):
        try:
            result = prepare_update_query_and_params(
                self.table_name,
                self.where_predicates,
                self.columns_data,
                True
            )
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, tuple)


if __name__ == '__main__':
    unittest.main()
