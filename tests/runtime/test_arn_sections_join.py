import unittest

from arcimoto.runtime import arn_sections_join

from tests._utility.constants import DEFAULT_TEST_LAMBDA_NAME


class TestArnSectionsJoin(unittest.TestCase):

    # test successes
    def test_arn_sections_join_success(self):
        try:
            result = arn_sections_join('lambda', DEFAULT_TEST_LAMBDA_NAME)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, str)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
