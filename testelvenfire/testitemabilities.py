import unittest
from elvenfire.abilities import AbilityError
from elvenfire.abilities.charabilities import MentalAbility, PhysicalAbility
from elvenfire.abilities.itemabilities import *


class TestAttributeAbility(unittest.TestCase):

    def testattributes(self):
        """Create each attribute, to ensure that no errors are encountered."""
        for attr in ('ST', 'DX', 'IQ', 'MA', 'Dam', 'Hit'):
            AttributeAbility([attr,])

    def testinvalidattribute(self):
        """Provide an invalid attribute, to generate an error."""
        self.assertRaises(AbilityError, AttributeAbility, 'Invalid')
        self.assertRaises(AbilityError, AttributeAbility, '', 3)

    def testattrlist(self):
        foundST = False
        foundDX = False
        for i in range(100):
            a = AttributeAbility(['ST', 'DX'])
            self.assert_(a.attr in ['ST', 'DX'])
            if a.attr == 'ST': foundST = True
            if a.attr == 'DX': foundDX = True
            if foundST and foundDX: break
        self.assert_(foundST and foundDX)

    def testdefaultattrlist(self):
        for i in range(50):
            a = AttributeAbility()
            self.assert_(a.attr in ('ST', 'DX', 'IQ', 'MA'))

    def testsize(self):
        """Create an attribute at each size."""
        for size in range(5):
            AttributeAbility(size=size + 1)

    def testinvalidsize(self):
        """Provide an invalid size, to generate an error."""
        self.assertRaises(AbilityError, AttributeAbility, size=0)
        self.assertRaises(AbilityError, AttributeAbility, size=6)

    def testAC(self):
        """Create each attribute ability and verify the Ability Cost."""
        for size in range(5):
            for attr in ('ST', 'DX'):
                a = AttributeAbility([attr,], size + 1)
                self.assertEqual(a.AC, (2000, 4000, 7000, 15000, 25000)[size])
            for attr in ('IQ', 'Dam'):
                a = AttributeAbility([attr,], size + 1)
                self.assertEqual(a.AC, (1000, 2000, 3500, 7000, 15000)[size])
            a = AttributeAbility(['MA',], size + 1)
            self.assertEqual(a.AC, (1000, 2000, 3000, 6000, 12000)[size])
            a = AttributeAbility(['Hit',], size + 1)
            self.assertEqual(a.AC, (1000, 2500, 5000, 10000, 18000)[size])

    def testMA(self):
        """Verify MA size is correctly doubled in display."""
        for size in range(5):
            a = AttributeAbility(['MA',], size + 1)
            self.assert_(str((size + 1) * 2) in str(a))
            self.assert_('MA' in str(a))

    def testduplicate(self):
        """Should return True any time the attribute matches."""
        a = AttributeAbility(['ST',], 3)
        self.assertTrue(a.duplicate(a))
        self.assertTrue(a.duplicate(AttributeAbility(['ST',], 3)))
        self.assertTrue(a.duplicate(AttributeAbility(['ST',], 5)))
        self.assertFalse(a.duplicate(AttributeAbility(['DX',], 5)))

    def testworsethan(self):
        """Should return True if the other has a higher size."""
        a = AttributeAbility(['ST',], 3)
        self.assertFalse(a.worsethan(a))
        self.assertFalse(a.worsethan(AttributeAbility(['ST',], 3)))
        self.assertFalse(a.worsethan(AttributeAbility(['ST',], 2)))
        self.assertTrue(a.worsethan(AttributeAbility(['ST',], 4)))


class TestAmuletAbility(unittest.TestCase):

    def testabilities(self):
        """Create each ability, to ensure no errors are encountered."""
        for ability in AmuletAbility.typelist:
            a = AmuletAbility(ability)
            self.assertEqual(a.type, ability)
            if ability != 'Attribute':
                self.assert_(ability in str(a))
            self.assertTrue(isinstance(a.AC, int))
            self.assertTrue(isinstance(a.description(), str))

    def testinvalidability(self):
        """Provide an invalid name, to generate an error."""
        self.assertRaises(AbilityError, AmuletAbility, 'Invalid')
        self.assertRaises(AbilityError, AmuletAbility, '')

    def testelements(self):
        """Provide each element in the initialization."""
        for element in AmuletAbility.elements:
            a = AmuletAbility('Proof', element=element)
            self.assert_(element in str(a))
            self.assertEqual(a.element, element)
            self.assertTrue(isinstance(a.AC, int))
            self.assertTrue(isinstance(a.description(), str))

    def testinvalidelement(self):
        """Provide an invalid element, to generate an error."""
        self.assertRaises(AbilityError, 
                          AmuletAbility, 'Proof', element='Invalid')
        self.assertRaises(AbilityError, AmuletAbility, 'Proof', element='')
        self.assertRaises(AbilityError, 
                          AmuletAbility, 'Control NPC', element='Fire')

    def testattributes(self):
        """Provide each attribute in the initialization."""
        for attr in AmuletAbility.attributes:
            a = AmuletAbility('Attribute', attr=attr)
            self.assert_(attr in str(a))
            self.assertEqual(a.attribute, attr)
            self.assertTrue(isinstance(a.AC, int))
            self.assertTrue(isinstance(a.description(), str))

    def testinvalidattribute(self):
        """Provide an invalid attribute, to generate an error."""
        self.assertRaises(AbilityError, AmuletAbility, 'Attribute', attr='Dam')
        self.assertRaises(AbilityError, AmuletAbility, 'Attribute', attr='')
        self.assertRaises(AbilityError, 
                          AmuletAbility, 'Control NPC', attr='ST')

    def testsize(self):
        """Provide each Skepticism size in the initialization."""
        for size in range(5):
            a = AmuletAbility('Skepticism', size=size+1)
            self.assert_(str(size+1) in str(a))
            self.assertEqual(a.size, size+1)
            self.assertTrue(isinstance(a.AC, int))
            self.assertTrue(isinstance(a.description(), str))

    def invalidsize(self):
        """Provide an invalid size, to generate an error."""
        self.assertRaises(AbilityError, AmuletAbility, 'Skepticism', size=0)
        self.assertRaises(AbilityError, AmuletAbility, 'Skepticism', size=6)
        self.assertRaises(AbilityError, AmuletAbility, 'Control NPC', size=3)

    def testequality(self):
        """Equal should be equal in all respects."""
        for i in range(len(AmuletAbility.typelist[:8])):  # no extra params
            type1 = AmuletAbility.typelist[i]
            self.assertEqual(AmuletAbility(type1), 
                             AmuletAbility(type1))
            for type2 in AmuletAbility.typelist[i+1:8]:
                self.assertNotEqual(AmuletAbility(type1), 
                                    AmuletAbility(type2))

        for i in range(len(AmuletAbility.elements)):
            e1 = AmuletAbility.elements[i]
            self.assertEqual(AmuletAbility('Proof', element=e1), 
                             AmuletAbility('Proof', element=e1))
            for e2 in AmuletAbility.elements[i+1:]:
                self.assertNotEqual(AmuletAbility('Proof', element=e1),
                                    AmuletAbility('Proof', element=e2))

        for i in range(len(AmuletAbility.attributes)):
            a1 = AmuletAbility.attributes[i]
            self.assertEqual(AmuletAbility('Attribute', attr=a1), 
                             AmuletAbility('Attribute', attr=a1))
            for a2 in AmuletAbility.attributes[i+1:]:
                self.assertNotEqual(AmuletAbility('Attribute', attr=a1), 
                                    AmuletAbility('Attribute', attr=a2))

        for s1 in range(1, 5):
            self.assertEqual(AmuletAbility('Skepticism', size=s1), 
                             AmuletAbility('Skepticism', size=s1))
            for s2 in range(s1 + 1, 5):
                self.assertNotEqual(AmuletAbility('Skepticism', size=s1), 
                                    AmuletAbility('Skepticism', size=s2))

    def testduplicate(self):
        """Should be true for different size Skepticism."""
        self.assertTrue(AmuletAbility('Control Dragon').duplicate(
                        AmuletAbility('Control Dragon')))
        self.assertFalse(AmuletAbility('Control Dragon').duplicate(
                         AmuletAbility('Control NPC')))
        self.assertTrue(AmuletAbility('Proof', element='Fire').duplicate(
                        AmuletAbility('Proof', element='Fire')))
        self.assertFalse(AmuletAbility('Proof', element='Fire').duplicate(
                         AmuletAbility('Proof', element='Water')))
        self.assertTrue(AmuletAbility('Attribute', attr='ST').duplicate(
                        AmuletAbility('Attribute', attr='ST')))
        self.assertFalse(AmuletAbility('Attribute', attr='ST').duplicate(
                         AmuletAbility('Attribute', attr='DX')))
        self.assertTrue(AmuletAbility('Skepticism', size=3).duplicate(
                        AmuletAbility('Skepticism', size=3)))
        self.assertTrue(AmuletAbility('Skepticism', size=3).duplicate(
                        AmuletAbility('Skepticism', size=5)))

    def testworsethan(self):
        """Only true for Skepticism size differences."""
        big = AmuletAbility('Skepticism', size=4)
        little = AmuletAbility('Skepticism', size=3)
        self.assertFalse(little.worsethan(little))
        self.assertFalse(little.worsethan(AmuletAbility('Skepticism', size=3)))
        self.assertTrue(little.worsethan(big))
        self.assertFalse(big.worsethan(little))

    def testrandom(self):
        """Ensure random abilities may be generated without error."""
        for i in range(100):
            AmuletAbility()


class TestWeaponAbility(unittest.TestCase):

    def testabilities(self):
        """Create each ability, to ensure that no errors are encountered."""
        for ability in WeaponAbility.typelist:
            a = WeaponAbility(ability)
            self.assert_(ability in str(a))
            self.assertTrue(isinstance(a.AC, int))
            self.assertTrue(isinstance(a.description(), str))

    def testinvalidability(self):
        """Provide an invalid ability name, to generate an error."""
        self.assertRaises(AbilityError, WeaponAbility, 'Invalid')
        self.assertRaises(AbilityError, WeaponAbility, '')

    def testrange(self):
        """Create each Animated weapon range, to ensure no errors occur."""
        for range_ in range(1, 5):
            a = WeaponAbility('Animated', range=range_)
            self.assert_(str(range_) in str(a))

    def testinvalidrange(self):
        """Provide an invalid range, to generate an error."""
        self.assertRaises(AbilityError, WeaponAbility, 'Animated', range=0)
        self.assertRaises(AbilityError, WeaponAbility, 'Animated', range=6)
        self.assertRaises(AbilityError, WeaponAbility, 'Animated', range='3')
        self.assertRaises(AbilityError, WeaponAbility, 'Changling', range=3)

    def testsize(self):
        """Create each Defender penalty size, to ensure no errors occur."""
        for size in range(1, 5):
            a = WeaponAbility('Defender', size=size)
            self.assert_(str(size) in str(a))

    def testinvalidsize(self):
        """Provide an invalid size, to generate an error."""
        self.assertRaises(AbilityError, WeaponAbility, 'Defender', size=0)
        self.assertRaises(AbilityError, WeaponAbility, 'Defender', size=6)
        self.assertRaises(AbilityError, WeaponAbility, 'Defender', size='3')
        self.assertRaises(AbilityError, WeaponAbility, 'Changling', size=3)

    def testenhancements(self):
        """Exercise the specification of abilities for Enhanced weapons."""
        list = [MentalAbility('Fireball', 3),]
        a = WeaponAbility('Enhanced', abilities=list)
        self.assertEqual(a.abilities, list)
        self.assertEqual(a.AC, list[0].AC)
        list *= 5
        a = WeaponAbility('Enhanced', abilities=list)
        self.assertEqual(a.abilities, list)
        self.assertEqual(a.AC, list[0].AC * (1 + 2 + 4 + 8 + 16))

    def testinvalidenhancements(self):
        """Provide invalid mental abilities, to generate errors."""
        self.assertRaises(AbilityError, 
                          WeaponAbility, 'Enhanced', abilities=[])
        list = [MentalAbility('Fireball', 3),] * 6
        self.assertRaises(AbilityError, 
                          WeaponAbility, 'Enhanced', abilities=list)
        list = [PhysicalAbility('Sword', 3),]
        self.assertRaises(AbilityError, 
                          WeaponAbility, 'Enhanced', abilities=list)
        list = [MentalAbility('Fireball', 3),] * 3
        self.assertRaises(AbilityError,
                          WeaponAbility, 'Guided', abilities=list)

    def testduplicate(self):
        """True if the types are the same."""
        self.assertTrue(WeaponAbility('Guided').duplicate(
                        WeaponAbility('Guided')))
        self.assertFalse(WeaponAbility('Guided').duplicate(
                         WeaponAbility('Changling')))
        self.assertTrue(WeaponAbility('Animated', range=1).duplicate(
                        WeaponAbility('Animated', range=3)))
        self.assertTrue(WeaponAbility('Defender', size=1).duplicate(
                        WeaponAbility('Defender', size=3)))
        fire = MentalAbility('Fireball')
        ice = MentalAbility('Iceball')
        self.assertTrue(WeaponAbility('Enhanced', abilities=[ice,]).duplicate(
                        WeaponAbility('Enhanced', abilities=[fire,])))

    def testworsethan(self):
        """True if the range/size/AC is higher."""
        large = WeaponAbility('Animated', range=3)
        small = WeaponAbility('Animated', range=2)
        self.assertFalse(small.worsethan(small))
        self.assertFalse(small.worsethan(WeaponAbility('Animated', range=2)))
        self.assertFalse(large.worsethan(small))
        self.assertTrue(small.worsethan(large))
        large = WeaponAbility('Defender', size=3)
        small = WeaponAbility('Defender', size=2)
        self.assertFalse(small.worsethan(small))
        self.assertFalse(small.worsethan(WeaponAbility('Defender', size=2)))
        self.assertFalse(large.worsethan(small))
        self.assertTrue(small.worsethan(large))
        abil = MentalAbility('Beacon', 1)
        large = WeaponAbility('Enhanced', abilities=[abil,])
        abil = MentalAbility('Avert', 2)
        small = WeaponAbility('Enhanced', abilities=[abil,])
        self.assertFalse(small.worsethan(small))
        self.assertFalse(small.worsethan(
                         WeaponAbility('Enhanced', abilities=[abil,])))
        self.assertFalse(large.worsethan(small))
        self.assertTrue(small.worsethan(large))

    def testrandom(self):
        """Ensure random abilities may be generated without error."""
        for i in range(100):
            WeaponAbility()


if __name__ == '__main__':
    unittest.main()






            