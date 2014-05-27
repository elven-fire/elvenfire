import unittest
from elvenfire.artifacts.special import *
from elvenfire.artifacts import ArtifactError
from elvenfire.abilities import AbilityError
from elvenfire.abilities.charabilities import *


class TestSpecialArtifact(unittest.TestCase):

    def testtypes(self):
        """Create one of every special artifact, to verify no errors occur."""
        for type in SpecialArtifact.typelist:
            s = SpecialArtifact(type)
            self.assertEqual(s.type, type)

    def testinvalidtype(self):
        """Provide an invalid type, to generate an error."""
        self.assertRaises(ArtifactError, SpecialArtifact, 'Invalid')
        self.assertRaises(ArtifactError, SpecialArtifact, '')

    def testability(self):
        """Exercise the specification of a Self-Powered Ring ability."""
        for name in MentalAbility.abilities.keys():
            ability = MentalAbility(name)
            s = SpecialArtifact('Self-Powered Ring', ability=ability)
            self.assertEqual(s.ability, ability)
            self.assertEqual(s.value, 25 * ability.AC)

    def testinvalidability(self):
        """Provide an invalid ability, to generate an error."""
        #pairability = MentalAbilityWithOpposites('Aid [+ Drain]')
        #self.assertRaises(ArtifactError, 
        #                  SpecialArtifact, 'Self-Powered Ring', 
        #                                   ability=pairability)
        phys = PhysicalAbility()
        self.assertRaises(ArtifactError,
                          SpecialArtifact, 'Self-Powered Ring', ability=phys)
        self.assertRaises(ArtifactError,
                          SpecialArtifact, 'Charm', ability=MentalAbility())

    def testIIQ(self):
        """Exercise the specification of IIQ for a Self-Powered Ring."""
        for IIQ in range(5):
            s = SpecialArtifact('Self-Powered Ring', IIQ=IIQ+1)
            self.assertEqual(s.ability.IIQ, IIQ + 1)

    def testinvalidIIQ(self):
        """Provide an invalid IIQ to generate an error."""
        self.assertRaises(AbilityError,
                          SpecialArtifact, 'Self-Powered Ring', IIQ=0)
        self.assertRaises(AbilityError,
                          SpecialArtifact, 'Self-Powered Ring', IIQ=6)
        self.assertRaises(AbilityError,
                          SpecialArtifact, 'Self-Powered Ring', IIQ='3')
        self.assertRaises(ArtifactError, SpecialArtifact, 'Charm', IIQ=3)

    def testcloakofvision(self):
        """Exercise ability/IIQ specification for a cloak of vision."""
        for IIQ in range(5):
            ability = MentalAbility('Vision', IIQ + 1)
            s = SpecialArtifact('Cloak of Vision', ability=ability)
            self.assertEqual(s.ability, ability)
            s = SpecialArtifact('Cloak of Vision', IIQ=IIQ+1)
            self.assertEqual(s.ability, ability)

    def testinvalidcloakofvision(self):
        """Generate errors by specifying invalid ability/IIQ."""
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Cloak of Vision', 
                                           ability=MentalAbility('Avert'))
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Cloak of Vision', 
                                           ability=PhysicalAbility())
        self.assertRaises(AbilityError,
                          SpecialArtifact, 'Cloak of Vision', IIQ=0)
        self.assertRaises(AbilityError,
                          SpecialArtifact, 'Cloak of Vision', IIQ=6)
        self.assertRaises(AbilityError,
                          SpecialArtifact, 'Cloak of Vision', IIQ='3')

    def testIQ(self):
        """Exercise IQ specification for a Gem of Summoning."""
        for IQ in range(9, 25):
            s = SpecialArtifact('Gem of Summoning', IQ=IQ)
            self.assertEqual(s.IQ, IQ)

    def testinvalidIQ(self):
        """Provide an invalid IQ to generate an error."""
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Gem of Summoning', IQ=0)
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Gem of Summoning', IQ=8)
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Gem of Summoning', IQ=26)
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Gem of Summoning', IQ='3')
        self.assertRaises(ArtifactError, SpecialArtifact, 'Charm', IQ=3)

    def testsize(self):
        """Exercise size specification for a Flying Carpet."""
        for size in range(1, 25):
            s = SpecialArtifact('Flying Carpet', size=size)
            self.assertEqual(s.size, size)

    def testinvalidsize(self):
        """Provide an invalid size to generate an error."""
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Flying Carpet', size=0)
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Flying Carpet', size=26)
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Flying Carpet', size='3')
        self.assertRaises(ArtifactError, 
                          SpecialArtifact, 'Shapeshifter', size=3)

    def testcharm(self):
        """Exercise the creation of charms of specific sizes."""
        self.assertRaises(ArtifactError, SpecialArtifact, 'Charm', size=0)
        self.assertEqual(SpecialArtifact('Charm', size=1).size, 1)
        self.assertEqual(SpecialArtifact('Charm', size=2).size, 2)
        self.assertRaises(ArtifactError, SpecialArtifact, 'Charm', size=3)
        self.assertRaises(ArtifactError, SpecialArtifact, 'Charm', size='1')

    def testautotype(self):
        """Verify that type is determined by other parameters."""
        for i in range(10):
            a = SpecialArtifact(ability=MentalAbility('Avert'))
            self.assertEqual(a.type, 'Self-Powered Ring')
            a = SpecialArtifact(ability=MentalAbility('Vision'))
            self.assert_(a.type in ('Self-Powered Ring', 'Cloak of Vision'))
            a = SpecialArtifact(IIQ=3)
            self.assert_(a.type in ('Self-Powered Ring', 'Cloak of Vision'))
            a = SpecialArtifact(IQ=12)
            self.assertEqual(a.type, 'Gem of Summoning')
            a = SpecialArtifact(size=5)
            self.assertEqual(a.type, 'Flying Carpet')
            a = SpecialArtifact(size=2)
            self.assert_(a.type in ('Flying Carpet', 'Charm'))

    def testrandom(self):
        """Ensure that artifacts can be randomly generated without errors."""
        for i in range(100):
            SpecialArtifact()


class TestSTBattery(unittest.TestCase):

    def testcharges(self):
        """Create each number of charges, to ensure no errors occur."""
        for c in range(25):
            r = STBattery(charges=c+1)
            self.assertEqual(r.charges, c + 1)
            self.assert_('%s charges' % (c + 1) in str(r))
        r = STBattery(3)
        self.assertEqual(r.charges, 3)

    def testinvalidcharges(self):
        """Provide invalid number of charges, to generate an error."""
        self.assertRaises(ArtifactError, STBattery, charges=-1)
        self.assertRaises(ArtifactError, STBattery, charges=0)
        self.assertRaises(ArtifactError, STBattery, charges=26)
        self.assertRaises(ArtifactError, STBattery, charges='10')

    def testvalue(self):
        """Verify that the value is being calculated correctly."""
        r = STBattery(1)
        self.assertEqual(r.value, 1000)
        r = STBattery(10)
        self.assertEqual(r.value, 10000)
        r = STBattery(20)
        self.assertEqual(r.value, 30000)
        r = STBattery(21)
        self.assertEqual(r.value, 33000)
        r = STBattery(22)
        self.assertEqual(r.value, 37000)
        r = STBattery(23)
        self.assertEqual(r.value, 42000)
        r = STBattery(24)
        self.assertEqual(r.value, 49000)
        r = STBattery(25)
        self.assertEqual(r.value, 59000)

    def testrandom(self):
        """Ensure that STBatteries can be randomly generated without errors."""
        for i in range(100):
            STBattery()


if __name__ == '__main__':
    unittest.main()





