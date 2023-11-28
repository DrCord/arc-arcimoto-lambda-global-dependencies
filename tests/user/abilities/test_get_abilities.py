import unittest

from arcimoto.user import Abilities


class TestGetAbilities(unittest.TestCase):

    test_ability = {'test ability': 'yep test'}

    # test successes
    def test_get_abilities_success(self):
        AbilitiesObject = Abilities(mock=True)
        self.assertFalse(AbilitiesObject.get_abilities())
        AbilitiesObject._abilities.append(self.test_ability)
        self.assertTrue(AbilitiesObject.get_abilities())

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
