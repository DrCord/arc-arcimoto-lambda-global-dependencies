import unittest

from arcimoto.runtime import (
    ENV_DEV,
    get_env
)


class TestGetEnv(unittest.TestCase):

    # test successes
    def test_get_env_success(self):
        try:
            result = get_env()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertEqual(result, ENV_DEV)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
