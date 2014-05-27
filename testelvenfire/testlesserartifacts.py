import unittest
from elvenfire.artifacts.lesser import *
from elvenfire.artifacts import ArtifactError
from elvenfire.abilities.itemabilities import AmuletAbility
from elvenfire.abilities.charabilities import *


class TestAmulet(unittest.TestCase):

    def testability(self):
        """Create an Amulet using each valid ability."""
        for name in AmuletAbility.typelist:
            a = Amulet(abilities=[AmuletAbility(name)])
            self.assertEqual(len(a.abilities), 1)
            self.assertEqual(a.value, a.abilities[0].AC)

    def testabilities(self):
        """Create an Amulet with multiple abilities; verify no errors occur."""
        list = []
        for i in range(5):
            list.append(AmuletAbility())
            a = Amulet(abilities=list)
            self.assertEqual(len(a.abilities), i + 1)

    def testinvalidability(self):
        """Provide an invalid ability, to generate an error."""
        self.assertRaises(ArtifactError, Amulet, abilities=[])
        list = [AmuletAbility()] * 6
        self.assertRaises(ArtifactError, Amulet, abilities=list)
        self.assertRaises(ArtifactError, Amulet, abilities=[MentalAbility()])

    def testvalue(self):
        ability = AmuletAbility()
        a = Amulet(abilities=[ability]*5)
        self.assertEqual(a.value, ability.AC * (1 + 2 + 4 + 8 + 16))
        list = [AmuletAbility('Control Trainable Riding Animal'), 
                AmuletAbility('Control Non-Trainable Insect')]
        a = Amulet(abilities = list)
        self.assertEqual(a.value, (3000 * 1 + 2000 * 2))

    def testrandom(self):
        """Ensure that Amulets can be randomly generated without errors."""
        for i in range(100):
            Amulet()


class TestGem(unittest.TestCase):

    def testability(self):
        """Create a gem with a specific ability, to ensure no errors occur."""
        for name in MentalAbilityWithOpposites.getabilities():
            ability = MentalAbilityWithOpposites(name)
            g = Gem(ability=ability)
            self.assertEqual(g.ability, ability)

    def testinvalidability(self):
        """Provide an invalid ability, to generate an error."""
        self.assertRaises(ArtifactError, Gem, ability=PhysicalAbility())
        self.assertRaises(ArtifactError, Gem, ability=AmuletAbility())

    def testvalue(self):
        """Verify that the value is being calculated correctly."""
        g = Gem()
        self.assertTrue(isinstance(g.value, int))
        self.assertEqual(g.value, round(g.ability.AC / 10))

    def testrandom(self):
        """Ensure that Gems can be randomly generated without errors."""
        for i in range(100):
            Gem()


if __name__ == '__main__':
    unittest.main()

