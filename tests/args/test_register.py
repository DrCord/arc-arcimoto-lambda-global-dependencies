from copy import deepcopy
import unittest

import arcimoto.args

from arcimoto.exceptions import ArcimotoArgumentError


class TestRegister(unittest.TestCase):

    test_schema = {
        'vin': {
            'type': 'string',
            'required': True
        }
    }

    # test successes
    def test_register_success(self):
        try:
            arcimoto.args.register(self.test_schema)
        except Exception as e:
            self.fail(f'test failed: {e}')
        arcimoto.args._validator = None

    # test errors
    def test_register_error(self):
        test_schema = deepcopy(self.test_schema)
        test_schema['vin']['magical_power'] = 17
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.args.register(test_schema)


if __name__ == '__main__':
    unittest.main()
