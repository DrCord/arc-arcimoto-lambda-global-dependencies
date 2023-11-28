from copy import deepcopy
import unittest

import arcimoto.args
from arcimoto.tests import uuid_vin_get

from arcimoto.exceptions import ArcimotoArgumentError


class TestValidate(unittest.TestCase):

    schema = {
        'vin': {
            'type': 'string',
            'required': True
        }
    }
    args = {
        'vin': uuid_vin_get()
    }

    @classmethod
    def setUpClass(cls):
        arcimoto.args._create_validator(cls.schema)

    @classmethod
    def tearDownClass(cls):
        arcimoto.args._validator = None

    # test successes
    def test_validate_success(self):
        try:
            arcimoto.args.validate(self.args)
        except Exception as e:
            self.fail(f'test failed: {e}')

    # test errors
    def test_validate_error_input_invalid_type(self):
        args = deepcopy(self.args)
        args['vin'] = self.args
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.args.validate(args)

    def test_validate_error_input_required_not_available(self):
        args = deepcopy(self.args)
        del args['vin']
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.args.validate(args)


if __name__ == '__main__':
    unittest.main()
