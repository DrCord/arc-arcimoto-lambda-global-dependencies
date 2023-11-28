import unittest

from arcimoto.user import Abilities


class TestReset(unittest.TestCase):

    test_ability = {'test ability': 'yep test'}

    # test successes
    def test_reset_success(self):
        AbilitiesObject = Abilities(mock=True)
        AbilitiesObject._abilities.append(self.test_ability)
        try:
            AbilitiesObject.reset()
        except Exception as e:
            self.fail(f'test failed: {e}')
        self.assertFalse(AbilitiesObject.abilities)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
