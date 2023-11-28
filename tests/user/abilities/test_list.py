import unittest

from arcimoto.user import Abilities


class TestList(unittest.TestCase):

    test_ability = {'test ability': 'yep test'}

    # test successes
    def test_list_success(self):
        AbilitiesObject = Abilities(mock=True)
        try:
            result = AbilitiesObject.list(mock=True)
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertIsInstance(result, str)
        self.assertIn('SELECT', result)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
