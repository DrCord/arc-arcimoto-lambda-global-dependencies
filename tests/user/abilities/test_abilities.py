import unittest

from arcimoto.user import Abilities


class TestAbilities(unittest.TestCase):

    test_ability = {'test ability': 'yep test'}

    # test successes
    def test_abilities_success_getter(self):
        AbilitiesObject = Abilities(mock=True)
        self.assertFalse(AbilitiesObject.abilities)
        AbilitiesObject._abilities.append(self.test_ability)
        self.assertTrue(AbilitiesObject.abilities)

    def test_abilities_success_setter(self):
        AbilitiesObject = Abilities(mock=True)
        self.assertFalse(AbilitiesObject.abilities)
        AbilitiesObject.abilities = [self.test_ability]
        self.assertTrue(AbilitiesObject.abilities)

    # test errors
    # None


if __name__ == '__main__':
    unittest.main()
