import unittest
from elvenfire.abilities import AbilityError
from elvenfire.abilities.charabilities import *


class TestPhysicalAbility(unittest.TestCase):

    def testabilities(self):
        """Create each ability, to ensure that no errors are encountered."""
        for ability in PhysicalAbility.abilities.keys():
            a = PhysicalAbility(ability)

    def testinvalidability(self):
        """Provide an invalid ability name, to generate an error."""
        self.assertRaises(AbilityError, PhysicalAbility, 'Invalid')
        self.assertRaises(AbilityError, PhysicalAbility, '')

    def testIIQ(self):
        """Create an ability at each IIQ."""
        for IIQ in range(5):
            PhysicalAbility(None, IIQ + 1)

    def testinvalidIIQ(self):
        """Provide an invalid IIQ, to generate an error."""
        self.assertRaises(AbilityError, PhysicalAbility, None, 0)
        self.assertRaises(AbilityError, PhysicalAbility, None, 6)

    def testunusuals(self):
        """Verify that the unusual weapon type can be specified correctly."""
        ability = 'Unusual Weapons'
        for element in PhysicalAbility.elements[ability]:
            a = PhysicalAbility(ability, 3, element)
            self.assertEqual(a.element, element)

    def testlanguages(self):
        """Verify that the language can be specified correctly."""
        ability = 'Literacy'
        for element in PhysicalAbility.elements[ability]:
            a = PhysicalAbility(ability, 3, element)
            self.assertEqual(a.element, element)

    def testinvalidelement(self):
        """Supply an element incorrectly, to generate an error."""
        self.assertRaises(AbilityError, PhysicalAbility,
                          'Unusual Weapons', 3, 'Electrical')
        self.assertRaises(AbilityError, PhysicalAbility,
                          'Literacy', 3, 'Electrical')
        self.assertRaises(AbilityError, PhysicalAbility,
                          'Sword', 3, 'Fire')

    def testequality(self):
        """Abilities with the same name and IIQ should be equal."""
        self.assertEqual(PhysicalAbility('Sword', 3), 
                         PhysicalAbility('Sword', 3))
        self.assertNotEqual(PhysicalAbility('Sword', 3), 
                            PhysicalAbility('Armor', 3))
        self.assertNotEqual(PhysicalAbility('Sword', 3), 
                            PhysicalAbility('Sword', 4))

    def testhash(self):
        """Should follow equality."""
        s3 = PhysicalAbility('Sword', 3)
        self.assertEqual(hash(s3), hash(s3))
        self.assertEqual(hash(s3), hash(PhysicalAbility('Sword', 3)))
        self.assertNotEqual(hash(s3), hash(PhysicalAbility('Armor', 3)))
        self.assertNotEqual(hash(s3), hash(PhysicalAbility('Sword', 4)))

    def testduplicate(self):
        """Checks abilities name and element only."""
        s3 = PhysicalAbility('Sword', 3)
        self.assertTrue(s3.duplicate(s3))
        self.assertTrue(s3.duplicate(PhysicalAbility('Sword', 3)))
        self.assertFalse(s3.duplicate(PhysicalAbility('Armor', 3)))
        self.assertTrue(s3.duplicate(PhysicalAbility('Sword', 4)))

    def testduplicateelement(self):
        """Checks abilities name and element only."""
        s3 = PhysicalAbility('Literacy', 3, 'Common')
        self.assertTrue(s3.duplicate(s3))
        self.assertTrue(s3.duplicate(PhysicalAbility('Literacy', 2, 'Common')))
        self.assertFalse(s3.duplicate(PhysicalAbility('Literacy', 3, 'Elvish')))

    def testworsethan(self):
        """Should always return False; should only be called when duplicates."""
        s3 = PhysicalAbility('Sword', 3)
        self.assertFalse(s3.worsethan(s3))
        self.assertFalse(s3.worsethan(PhysicalAbility('Sword', 3)))

    def testmethods(self):
        """Test each public property and method, for each ability/IIQ."""
        for ability in PhysicalAbility.abilities.keys():
            for IIQ in range(1, 5):
                if ability == 'Leadership' and IIQ > 3: continue
                if ability == 'Pole Weapons' and IIQ > 4: continue
                a = PhysicalAbility(ability, IIQ)
                self.assertTrue(isinstance(str(a), str))
                self.assertTrue(isinstance(a.description(), str))
                self.assertTrue(isinstance(a.baseAC, int))
                self.assertTrue(isinstance(a.AC, int))
                self.assertEqual(a.baseAC, 
                                   PhysicalAbility.abilities[ability])
                self.assertEqual(a.baseAC * (1, 2, 3, 6, 12)[IIQ-1],
                                 a.AC)
                self.assertEqual(a.description(), str(a) + ': ' +
                                 PhysicalAbility.abilitydescs[ability][IIQ-1])

                if ability.startswith('Unusual Weapons'):
                    self.assertTrue(isinstance(a.element, str))
                    self.assertIn(a.element, PhysicalAbility.elements[ability])
                    self.assertIn(a.element, str(a))

                elif ability.startswith('Literacy'):
                    self.assertTrue(isinstance(a.element, str))
                    self.assertIn(a.element, PhysicalAbility.elements[ability])
                    self.assertIn(a.element, str(a))

                else:
                    self.assertIs(a.element, None)

        ## will fail on missing: see testmissing() below

    def testrandom(self):
        """Ensure random abilities may be generated without error."""
        for i in range(100):
            PhysicalAbility()

    def testmissing(self):
        """Ensure missing ability IIQs are corrected."""
        self.assertEqual(PhysicalAbility('Leadership', 4).IIQ, 3)
        self.assertEqual(PhysicalAbility('Leadership', 5).IIQ, 3)
        self.assertEqual(PhysicalAbility('Pole Weapons', 5).IIQ, 4)



class TestMentalAbility(unittest.TestCase):

    def testabilities(self):
        """Create each ability, to ensure that no errors are encountered."""
        for ability in MentalAbility.abilities.keys():
            a = MentalAbility(ability)

    def testinvalidability(self):
        """Provide an invalid ability name, to generate an error."""
        self.assertRaises(AbilityError, MentalAbility, 'Invalid')
        self.assertRaises(AbilityError, MentalAbility, '')

    def testIIQ(self):
        """Create an ability at each IIQ."""
        for IIQ in range(5):
            MentalAbility(None, IIQ + 1)

    def testinvalidIIQ(self):
        """Provide an invalid IIQ, to generate an error."""
        self.assertRaises(AbilityError, MentalAbility, None, 0)
        self.assertRaises(AbilityError, MentalAbility, None, 6)

    def testequality(self):
        """Abilities with the same name and IIQ should be equal."""
        self.assertEqual(MentalAbility('Fireball', 3), 
                         MentalAbility('Fireball', 3))
        self.assertNotEqual(MentalAbility('Fireball', 3), 
                            MentalAbility('Iceball', 3))
        self.assertNotEqual(MentalAbility('Fireball', 3), 
                            MentalAbility('Fireball', 4))

    def testhash(self):
        """Should follow equality."""
        s3 = MentalAbility('Fireball', 3)
        self.assertEqual(hash(s3), hash(s3))
        self.assertEqual(hash(s3), hash(MentalAbility('Fireball', 3)))
        self.assertNotEqual(hash(s3), hash(MentalAbility('Iceball', 3)))
        self.assertNotEqual(hash(s3), hash(MentalAbility('Fireball', 4)))

    def testduplicate(self):
        """Compares ability name and element only."""
        s3 = MentalAbility('Fireball', 3)
        self.assertTrue(s3.duplicate(s3))
        self.assertTrue(s3.duplicate(MentalAbility('Fireball', 3)))
        self.assertFalse(s3.duplicate(MentalAbility('Iceball', 3)))
        self.assertTrue(s3.duplicate(MentalAbility('Fireball', 4)))

    def testduplicateelement(self):
        """Checks abilities name and element only."""
        s3 = MentalAbility('Create', 3, 'Wall')
        self.assertTrue(s3.duplicate(s3))
        self.assertTrue(s3.duplicate(MentalAbility('Create', 2, 'Wall')))
        self.assertFalse(s3.duplicate(MentalAbility('Create', 3, 'Fire')))

    def testworsethan(self):
        """Should always return False; should only be called when duplicates."""
        s3 = MentalAbility('Fireball', 3)
        self.assertFalse(s3.worsethan(s3))
        self.assertFalse(s3.worsethan(MentalAbility('Fireball', 3)))

    def testmethods(self):
        """Test each public property and method, for each ability/IIQ."""
        for ability in MentalAbility.abilities.keys():
            for IIQ in range(5):
                a = MentalAbility(ability, IIQ + 1)
                self.assertTrue(isinstance(str(a), str))
                self.assertTrue(isinstance(a.description(), str))
                self.assertTrue(isinstance(a.baseAC, int))
                self.assertTrue(isinstance(a.AC, int))
                self.assertEqual(a.baseAC, 
                                   MentalAbility.abilities[ability])
                self.assertEqual(a.baseAC * (1, 2, 3, 6, 12)[IIQ],
                                 a.AC)
                self.assertEqual(a.description(), str(a) + ': ' +
                                 MentalAbility.abilitydescs[ability][IIQ])

                if (ability.startswith('Proof') or
                    ability.startswith('Sensitize') or
                    ability.startswith('Storm') or
                    ability.startswith('Calm')):
                    self.assertTrue(isinstance(a.element, str))
                    self.assertIn(a.element, MentalAbility.elements[ability])
                    self.assertIn(a.element, str(a))

                elif ((ability.startswith('Create') and 
                     not ability.startswith('Create Artifact')) or
                    (ability.startswith('Destroy') and
                     not ability.startswith('Destroy Artifact'))):
                    self.assertTrue(isinstance(a.element, str))
                    self.assertIn(a.element, MentalAbility.elements[ability])
                    self.assertIn(a.element, str(a))

                else:
                    self.assertIs(a.element, None)

    def testEtherealBow(self):
        """Verify supplying 'Ethereal Bow' works correctly."""
        for i in range(25):
            a = MentalAbility('Ethereal Bow')
            self.assert_(a.name in MentalAbility.EtherealBow)

    def testelement(self):
        """Verify that the element can be specified correctly."""
        for ability in ('Proof', 'Sensitize', 'Storm', 'Calm'):
            for element in MentalAbility.elements[ability]:
                a = MentalAbility(ability, 3, element)
                self.assertEqual(a.element, element)

    def testinvalidelement(self):
        """Supply an element incorrectly, to generate an error."""
        self.assertRaises(AbilityError, MentalAbility, 'Proof', 3, 'Shadow')
        self.assertRaises(AbilityError, MentalAbility, 'Fireball', 3, 'Fire')

    def testcreatable(self):
        """Verify that the creation element can be specified correctly."""
        for ability in ('Create', 'Destroy'):
            for element in MentalAbility.elements[ability]:
                a = MentalAbility(ability, 3, element)
                self.assertEqual(a.element, element)

    def testinvalidcreatable(self):
        """Supply an element incorrectly, to generate an error."""
        self.assertRaises(AbilityError, MentalAbility, 'Create', 3, 
                                                       'Electrical')
        self.assertRaises(AbilityError, MentalAbility, 'Create Artifact', 3, 
                                                       'Fire')

    def testrandom(self):
        """Ensure random abilities may be generated without error."""
        for i in range(100):
            MentalAbility()


class TestMentalAbilityWithOpposites(unittest.TestCase):

    def testpairs(self):
        """Ensure all paired abilities are valid mental abilities."""
        for (p, o) in MentalAbilityWithOpposites.pairs.items():
            self.assert_(p in MentalAbility.abilities.keys())
            self.assert_(o in MentalAbility.abilities.keys())

    def testopposite(self):
        """Ensure opposite=True functions as expected."""
        for i in range(100):
            a = MentalAbilityWithOpposites(opposite=True)
            self.assertIn("+", str(a))

    def testgetabilities(self):
        """Ensure getabilities() correctly returns singles plus pairs."""
        list = MentalAbilityWithOpposites.getabilities()
        self.assertFalse(set(MentalAbility.abilities.keys()) - set(list))
        mylist = ['%s [+ %s]' % (p, o) for (p, o) 
                  in MentalAbilityWithOpposites.pairs.items()]
        self.assertEqual(set(list) - set(MentalAbility.abilities.keys()),
                         set(mylist))

    def testabilities(self):
        """Create each ability, to ensure that no errors are encountered."""
        for ability in MentalAbilityWithOpposites.getabilities():
            a = MentalAbilityWithOpposites(ability)

    def testinvalidability(self):
        """Provide an invalid ability name, to generate an error."""
        self.assertRaises(AbilityError, MentalAbilityWithOpposites, 'Invalid')
        self.assertRaises(AbilityError, MentalAbilityWithOpposites, '')
        self.assertRaises(AbilityError, 
                          MentalAbilityWithOpposites, 'Drain [+ Aid]')

    def testequality(self):
        """Singles vs pairs are considered inequal."""
        self.assertEqual(MentalAbilityWithOpposites('Aid', 3), 
                         MentalAbilityWithOpposites('Aid', 3))
        self.assertNotEqual(MentalAbilityWithOpposites('Aid', 3), 
                            MentalAbilityWithOpposites('Drain', 3))
        self.assertNotEqual(MentalAbilityWithOpposites('Aid', 3), 
                            MentalAbilityWithOpposites('Aid', 4))
        self.assertNotEqual(MentalAbilityWithOpposites('Aid', 3), 
                            MentalAbilityWithOpposites('Aid [+ Drain]', 3))

    def testhash(self):
        """Should follow equality."""
        s3 = MentalAbilityWithOpposites('Aid', 3)
        self.assertEqual(hash(s3), hash(s3))
        self.assertEqual(hash(s3), hash(MentalAbilityWithOpposites('Aid', 3)))
        self.assertNotEqual(hash(s3), hash(MentalAbilityWithOpposites('Drain', 3)))
        self.assertNotEqual(hash(s3), hash(MentalAbilityWithOpposites('Aid', 4)))
        self.assertNotEqual(hash(s3), 
                            hash(MentalAbilityWithOpposites('Aid [+ Drain]', 3)))

    def testduplicate(self):
        """Singles are considered duplicates of the matching pairs."""
        s3 = MentalAbilityWithOpposites('Aid', 3)
        self.assertTrue(s3.duplicate(s3))
        self.assertTrue(s3.duplicate(MentalAbilityWithOpposites('Aid', 3)))
        self.assertFalse(s3.duplicate(MentalAbilityWithOpposites('Drain', 3)))
        self.assertTrue(s3.duplicate(MentalAbilityWithOpposites('Aid', 4)))
        s4 = MentalAbilityWithOpposites('Drain', 3)
        pair = MentalAbilityWithOpposites('Aid [+ Drain]', 3)
        self.assertTrue(s3.duplicate(pair))
        self.assertTrue(s4.duplicate(pair))
        self.assertTrue(pair.duplicate(s3))
        self.assertTrue(pair.duplicate(s4))

    def testduplicateelement(self):
        """Checks abilities name and element only."""
        s3 = MentalAbilityWithOpposites('Create', 3, 'Fire')
        self.assertTrue(s3.duplicate(MentalAbilityWithOpposites('Create [+ Destroy]', 3, 'Fire')))
        self.assertFalse(s3.duplicate(MentalAbilityWithOpposites('Proof', 3, 'Fire')))
        self.assertFalse(s3.duplicate(MentalAbilityWithOpposites('Create', 3, 'Wall')))
                       
    def testworsethanpair(self):
        """Should return True only on singles vs matching pairs."""
        aid3 = MentalAbilityWithOpposites('Aid', 3)
        drain3 = MentalAbilityWithOpposites('Drain', 3)
        pair3 = MentalAbilityWithOpposites('Aid [+ Drain]', 3)
        self.assertFalse(aid3.worsethan(aid3))
        self.assertFalse(aid3.worsethan(drain3))
        self.assertFalse(aid3.worsethan(MentalAbilityWithOpposites('Aid', 3)))
        self.assertTrue(aid3.worsethan(pair3))
        self.assertTrue(drain3.worsethan(pair3))
        self.assertFalse(pair3.worsethan(aid3))
        self.assertFalse(pair3.worsethan(drain3))

    def testworsethanIIQ(self):
        """IIQ comparison should override singles/pair comparison."""
        aid4 = MentalAbilityWithOpposites('Aid', 4)
        pair3 = MentalAbilityWithOpposites('Aid [+ Drain]', 3)
        self.assertFalse(aid4.worsethan(pair3))
        self.assertTrue(pair3.worsethan(aid4))

    def testmethods(self):
        """Test each public property and method, for each ability/IIQ."""
        for ability in MentalAbilityWithOpposites.getabilities():
            for IIQ in range(5):
                a = MentalAbilityWithOpposites(ability, IIQ + 1, opposite=False)
                self.assertTrue(isinstance(str(a), str))
                self.assertTrue(isinstance(a.description(), str))
                self.assertTrue(isinstance(a.baseAC, int))
                self.assertTrue(isinstance(a.AC, int))
                self.assertEqual(a.AC, a.baseAC * (1, 2, 3, 6, 12)[IIQ])

    def testpairdescs(self):
        """Verify descriptions are generated correctly for pairs."""
        for (p, o) in MentalAbilityWithOpposites.pairs.items():
            for IIQ in range(1, 5):
                pairname = '%s [+ %s]' % (p, o)
                a = MentalAbilityWithOpposites(pairname, IIQ)
                mydesc = '%s: %s -- OR -- %s' % (str(a),
                                      MentalAbility.abilitydescs[p][IIQ-1],
                                      MentalAbility.abilitydescs[o][IIQ-1])
                self.assertEqual(a.description(), mydesc)

    def testopposite(self):
        """Verify the opposite= parameter."""
        a = MentalAbilityWithOpposites('Aid', opposite=True)
        self.assertEqual(a.name, 'Aid [+ Drain]')
        self.assertRaises(AbilityError,
                          MentalAbilityWithOpposites, 'Beacon', opposite=True)
        for i in range(50):
            a = MentalAbilityWithOpposites('Aid', opposite=False)
            self.assertEqual(a.name, 'Aid')

    def testautoopposite(self):
        """Verify that opposites are sometimes applied by default."""
        foundsingle = False
        foundpair = False
        for i in range(100):
            a = MentalAbilityWithOpposites()
            if '+' in a.name:
                foundpair = True
            else:
                foundsingle = True
            if foundsingle and foundpair:
                break
        self.assertTrue(foundsingle and foundpair)

    def testrandom(self):
        """Ensure random abilities may be generated without error."""
        for i in range(100):
            MentalAbilityWithOpposites()



class TestFactories(unittest.TestCase):

    def testrandomability(self):
        """Ensure random abilities may be generated without error."""
        for i in range(100):
            PhysicalOrMentalAbility()

    def testuniversityability(self):
        """Ensure random abilities may be generated without error."""
        for i in range(100):
            UniversityAbility()


if __name__ == '__main__':
    unittest.main()
