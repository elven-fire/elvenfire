import unittest
from elvenfire.artifacts.greater import *
from elvenfire.artifacts import ArtifactError
from elvenfire.abilities.charabilities import *


class TestRod(unittest.TestCase):

    def testcharges(self):
        """Create each number of charges, to ensure no errors occur."""
        for c in range(25):
            r = Rod(charges=c+1)
            self.assertEqual(r.charges, c + 1)
            self.assert_('%s charges' % (c + 1) in str(r))
        r = Rod(3)
        self.assertEqual(r.charges, 3)

    def testinvalidcharges(self):
        """Provide invalid number of charges, to generate an error."""
        self.assertRaises(ArtifactError, Rod, charges=-1)
        self.assertRaises(ArtifactError, Rod, charges=0)
        self.assertRaises(ArtifactError, Rod, charges=26)
        self.assertRaises(ArtifactError, Rod, charges='10')

    def testability(self):
        """Create a rod with a specific ability, to ensure no errors occur."""
        for name in MentalAbility.EtherealBow:
            ability = MentalAbility(name)
            r = Rod(ability=ability)
            self.assertEqual(r.ability, ability)

    def testinvalidability(self):
        """Provide an invalid ability, to generate an error."""
        self.assertRaises(ArtifactError, Rod, ability=MentalAbility('Avert'))
        self.assertRaises(ArtifactError, Rod, ability=PhysicalAbility('Sword'))

    def testvalue(self):
        """Verify that the value is being calculated correctly."""
        r = Rod(1)
        self.assertEqual(r.value, 1000 + r.ability.AC)
        r = Rod(10)
        self.assertEqual(r.value, 10000 + r.ability.AC)
        r = Rod(20)
        self.assertEqual(r.value, 30000 + r.ability.AC)

    def testrandom(self):
        """Ensure that Rods can be randomly generated without errors."""
        for i in range(100):
            Rod()


class TestRing(unittest.TestCase):

    def testability(self):
        """Create a Ring using each valid ability, to verify no errors occur."""
        for name in MentalAbilityWithOpposites.getabilities():
            r = Ring(abilities=[MentalAbilityWithOpposites(name)])
            self.assertEqual(len(r.abilities), 1)
            self.assertEqual(r.value, r.abilities[0].AC)

    def testabilities(self):
        """Create a Ring with multiple abilities, to verify no errors occur."""
        list = []
        for i in range(5):
            list.append(MentalAbility())
            r = Ring(abilities=list)
            self.assertEqual(len(r.abilities), i + 1)

    def testinvalidability(self):
        """Provide an invalid ability, to generate an error."""
        self.assertRaises(ArtifactError, Ring, abilities=[])
        list = [MentalAbility()] * 6
        self.assertRaises(ArtifactError, Ring, abilities=list)
        self.assertRaises(ArtifactError, Ring, abilities=[PhysicalAbility()])

    def testvalue(self):
        ability = MentalAbility('Aid', 1)
        r = Ring(abilities=[ability]*5)
        self.assertEqual(r.value, ability.AC * (1 + 2 + 4 + 8 + 16))
        list = [MentalAbility('Destroy Artifact', 1), MentalAbility('Aid', 1)]
        r = Ring(abilities = list)
        self.assertEqual(r.value, (1000 * 1 + 500 * 2))

    def testrandom(self):
        """Ensure that Rings can be randomly generated without errors."""
        for i in range(100):
            Ring()


if __name__ == '__main__':
    unittest.main()




