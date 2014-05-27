import unittest
from elvenfire.artifacts.potion import *
from elvenfire.artifacts import ArtifactError
from elvenfire.abilities import AbilityError
from elvenfire.abilities.charabilities import *


class TestHealingPotion(unittest.TestCase):

    def testdoses(self):
        """Create each number of doses, to ensure no errors occur."""
        for c in range(1, 25):
            r = HealingPotion(doses=c)
            self.assertEqual(r.doses, c)
            self.assert_('%s points' % (c) in str(r))
            self.assertEqual(r.value, 50 * c)
        r = HealingPotion(3)
        self.assertEqual(r.doses, 3)

    def testinvaliddoses(self):
        """Provide invalid number of doses, to generate an error."""
        self.assertRaises(ArtifactError, HealingPotion, doses=-1)
        self.assertRaises(ArtifactError, HealingPotion, doses=0)
        #self.assertRaises(ArtifactError, HealingPotion, doses=26)
        self.assertRaises(ArtifactError, HealingPotion, doses='10')

    def testrandom(self):
        """Ensure they can be randomly generated without errors."""
        for i in range(100):
            HealingPotion()


class TestWeaponPoison(unittest.TestCase):

    def testdamage(self):
        """Create each damage type, to ensure no errors occur."""
        for dmg in WeaponPoison.sizelist:
            w = WeaponPoison(dmg)
            self.assertTrue(w.dmg.startswith(dmg))

    def testinvaliddamage(self):
        """Provide invalid damage type, to generate an error."""
        self.assertRaises(ArtifactError, WeaponPoison, 'Invalid')
        self.assertRaises(ArtifactError, WeaponPoison, '')

    def testtype(self):
        """Exercise specification of target type."""
        for type in WeaponPoison.typelist:
            w = WeaponPoison('+d20 vs', type=type)
            self.assertEqual(w.type, type)

    def testinvalidtype(self):
        """Provide invalid target type, to generate an error."""
        self.assertRaises(ArtifactError, WeaponPoison, '+d20 vs', 'Invalid')
        self.assertRaises(ArtifactError, WeaponPoison, '+d20 vs', '')
        self.assertRaises(ArtifactError, WeaponPoison, 'Dam +d6', 'Dragons')

    def testdoses(self):
        """Verify that doses are provided for the correct poisons."""
        for dmg in WeaponPoison.sizelist:
            if dmg in ('Dam +d12', 'Dam +d10'):
                for doses in range(1, 4):
                    w = WeaponPoison(dmg, doses=doses)
                    self.assertEqual(w.doses, doses)
            else:
                self.assertRaises(ArtifactError, WeaponPoison, dmg, doses=2)

    def testinvaliddoses(self):
        """Provide invalid doses, to generate an error."""
        for dmg in ('Dam +d12', 'Dam +d10'):
            self.assertRaises(ArtifactError, WeaponPoison, dmg, doses=0)
            self.assertRaises(ArtifactError, WeaponPoison, dmg, doses=5)
            self.assertRaises(ArtifactError, WeaponPoison, dmg, doses='1')

    def testrandom(self):
        """Ensure they can be randomly generated without errors."""
        for i in range(100):
            WeaponPoison()


class TestGrenade(unittest.TestCase):

    def testdamage(self):
        """Create each damage type, to ensure no errors occur."""
        for dmg in Grenade.sizelist:
            w = Grenade(dmg)
            self.assertEqual(w.dmg, dmg)
            self.assert_(dmg in str(w))

    def testinvaliddamage(self):
        """Provide invalid damage type, to generate an error."""
        self.assertRaises(ArtifactError, Grenade, 'Invalid')
        self.assertRaises(ArtifactError, Grenade, '')

    def testtype(self):
        """Exercise specification of grenade type."""
        for type in Grenade.typelist:
            w = Grenade(type=type)
            self.assertEqual(w.type, type)
            self.assert_(type in str(w))

    def testinvalidtype(self):
        """Provide invalid target type, to generate an error."""
        self.assertRaises(ArtifactError, Grenade, type='Invalid')
        self.assertRaises(ArtifactError, Grenade, type='')

    def testrandom(self):
        """Ensure they can be randomly generated without errors."""
        for i in range(100):
            Grenade()


class TestAttributePotion(unittest.TestCase):

    def testattribute(self):
        """Create a potion with a specific attr, to ensure no errors occur."""
        for attr in AttributePotion.attributes:
            p = AttributePotion(attr=attr)
            self.assertEqual(p.ability.attr, attr)

            for size in range(1, 5):
                ability = AttributeAbility(attr, size)
                p1 = AttributePotion(ability=ability)
                p2 = AttributePotion(attr=attr, size=size)
                self.assertEqual(p1.ability, p2.ability)
                self.assertEqual(p1.ability, ability)
                self.assertEqual(p1, p2)

                p = AttributePotion(size=size)
                self.assertEqual(p.ability.size, size)

    def testinvalid(self):
        """Provide an invalid ability, to generate an error."""
        self.assertRaises(ArtifactError, 
                          AttributePotion, ability=MentalAbility('Avert'))
        self.assertRaises(ArtifactError, AttributePotion, attr='Dam')
        self.assertRaises(AbilityError, AttributePotion, size=0)
        self.assertRaises(AbilityError, AttributePotion, size=6)

    def testrandom(self):
        """Ensure they can be randomly generated without errors."""
        for i in range(100):
            AttributePotion()


class TestAbilityPotion(unittest.TestCase):

    def testability(self):
        """Give a specific ability, to ensure no errors occur."""
        for name in MentalAbility.abilities.keys():
            ability = MentalAbility(name)
            r = AbilityPotion(ability=ability)
            self.assertEqual(r.ability, ability)

    def testinvalidability(self):
        """Provide an invalid ability, to generate an error."""
        SWORD = PhysicalAbility('Sword')
        self.assertRaises(ArtifactError, AbilityPotion, ability=SWORD)

    def testIIQ(self):
        """Exercize specification of IIQ."""
        for IIQ in range(1, 5):
            p = AbilityPotion(IIQ=IIQ)
            self.assertEqual(p.ability.IIQ, IIQ)

    def testinvalidIIQ(self):
        """Provide an invalid IIQ to generate an error."""
        self.assertRaises(AbilityError, AbilityPotion, IIQ=0)
        self.assertRaises(AbilityError, AbilityPotion, IIQ=6)
        self.assertRaises(AbilityError, AbilityPotion, IIQ='3')

    def testrandom(self):
        """Ensure they can be randomly generated without errors."""
        for i in range(100):
            AbilityPotion()


class TestSpecialPotion(unittest.TestCase):

    def testtypes(self):
        """Specify each type to ensure no errors occur."""
        for type in SpecialPotion.typelist:
            p = SpecialPotion(type)
            self.assertEqual(p.name, type)

    def testrandom(self):
        """Ensure they can be randomly generated without errors."""
        for i in range(100):
            SpecialPotion()


class TestPotion(unittest.TestCase):

    def testrandom(self):
        """Ensure they can be randomly generated without errors."""
        for i in range(100):
            p = Potion()
            self.assert_(p.cls in [HealingPotion, WeaponPoison, Grenade,
                                   AttributePotion, AbilityPotion,
                                   SpecialPotion])


if __name__ == '__main__':
    unittest.main()
