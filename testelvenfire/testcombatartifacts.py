import unittest
from elvenfire.artifacts.combat import *
from elvenfire.artifacts import ArtifactError
from elvenfire.mundane import ItemError
from elvenfire.abilities.itemabilities import *
from elvenfire.abilities.charabilities import *


class TestWeapon(unittest.TestCase):

    def testlongweaponlist(self):
        """Verify that _longweaponlist() works for each style."""
        self.assertEqual(Weapon._longweaponlist(None),
                         Weapon.weaponlistings)
        for style in Weapon.stylelist:
            for listing in Weapon._longweaponlist(style):
                self.assertEqual(style, listing[1])

    def testpseudostyles(self):
        """Verify that each pseudostyle is interpreted correctly."""
        self.assertEqual(Weapon.pseudostyles, 
                         ['Missile Weapon', 'Two-Handed', 'Thrown Weapon',
                          'Hand-to-Hand', 'Crushing'])
        for listing in Weapon._longweaponlist('Missile Weapon'):
            self.assertIn('Bow', listing[1])  # Drawn/Cross Bow
        for listing in Weapon._longweaponlist('Two-Handed'):
            self.assertTrue(listing[4])
        for listing in Weapon._longweaponlist('Thrown Weapon'):
            self.assertTrue(listing[5])
        for listing in Weapon._longweaponlist('Crushing'):
            self.assertTrue(listing[6])
        for listing in Weapon._longweaponlist('Hand-to-Hand'):
            self.assertTrue(listing[7])

    def testweaponlist(self):
        """Verify that weaponlist() correctly returns the names."""
        for style in ([None,] + Weapon.stylelist + Weapon.pseudostyles):
            self.assertEqual(Weapon.weaponlist(style),
                             [i[0] for i in 
                              Weapon._longweaponlist(style)])

    def testisdistance(self):
        """Verify isdistance()."""
        distancelist = set(Weapon.weaponlist('Missile Weapon') +
                           Weapon.weaponlist('Thrown Weapon'))
        for listing in Weapon.weaponlistings:
            w = Weapon(type=listing[0])
            if listing[0] in distancelist:
                self.assertTrue(w.isdistance())
            else:
                self.assertFalse(w.isdistance())

    def teststyles(self):
        """Create a weapon using each style, to ensure no errors occur."""
        for style in ([None,] + Weapon.stylelist + Weapon.pseudostyles):
            w = Weapon(style=style)

    def testinvalidstyle(self):
        """Provide an invalid style, to generate an error."""
        self.assertRaises(ItemError, Weapon, style='Invalid')
        self.assertRaises(ItemError, Weapon, style='')

    def testtypes(self):
        """Create a weapon using each type, to ensure no errors occur."""
        for type in Weapon.weaponlist(None):
            w = Weapon(type=type)

    def testinvalidtype(self):
        """Provide an invalid type, to generate an error."""
        self.assertRaises(ItemError, Weapon, type='Invalid')
        self.assertRaises(ItemError, Weapon, type='')

    def teststylewithtype(self):
        """Provide both style and type."""
        # Set secondary=True to prevent Changling weapons...
        w = Weapon(style='Sword', type='Broadsword', secondary=True)
        self.assertEqual(w.style, 'Sword')
        self.assertEqual(w.type, 'Broadsword')
        self.assertRaises(ItemError, Weapon, style='Sword', 
                                                type='Pike',
                                                secondary=True)

    def testabilities(self):
        """Exercise the specification of abilities."""
        list = [AttributeAbility('ST', 5),]
        w = Weapon(abilities=list)
        self.assertEqual(w.abilities, list)
        self.assertEqual(w.value, list[0].AC)
        list *= 5
        w = Weapon(abilities=list)
        self.assertEqual(w.abilities, list)
        self.assertEqual(w.value, list[0].AC * (1 + 2 + 4 + 8 + 16))
        list = [WeaponAbility('Flaming'),]
        w = Weapon(abilities=list)
        self.assertEqual(w.abilities, list)
        self.assertEqual(w.value, list[0].AC)
        list *= 5
        w = Weapon(abilities=list)
        self.assertEqual(w.abilities, list)
        self.assertEqual(w.value, list[0].AC * (1 + 2 + 4 + 8 + 16))

    def testinvalidabilities(self):
        """Provide invalid weapon abilities, to generate errors."""
        self.assertRaises(ArtifactError, Weapon, abilities=[])
        list = [WeaponAbility('Flaming'),] * 6
        self.assertRaises(ArtifactError, Weapon, abilities=list)
        self.assertRaises(ArtifactError, 
                          Weapon, abilities=[AmuletAbility(),])
        self.assertRaises(ArtifactError, 
                          Weapon, abilities=[MentalAbility(),])

    def testsecondary(self):
        """secondary=True should prevent normal handling of Changlings."""
        CHANGLING = WeaponAbility('Changling')
        w = Weapon(abilities=[CHANGLING,], secondary=False)
        self.assert_('primaryweapon' in dir(w))
        w = Weapon(abilities=[CHANGLING,], secondary=True)
        self.assert_('primaryweapon' not in dir(w))
        GUIDED = WeaponAbility('Guided')
        self.assertRaises(ArtifactError, Weapon, type='Broadsword',
                                                 abilities=[GUIDED,],
                                                 secondary=True)

    def testguided(self):
        """Guided weapons must be distance."""
        GUIDED = WeaponAbility('Guided')
        for i in range(100):
            w = Weapon(abilities=[GUIDED,])
            self.assertTrue(w.isdistance())
        for i in range(100):
            w = Weapon(type='Broadsword')
            self.assert_(GUIDED not in w.abilities)
        self.assertRaises(ArtifactError, Weapon, type='Broadsword',
                                                 abilities=[GUIDED,])

    def testchangling(self):
        """Special handling for Changling weapons."""
        CHANGLING = WeaponAbility('Changling')
        DX = AttributeAbility('DX', 1)
        ST = AttributeAbility('DX', 1)

        # Test with secondary as missile weapon
        w = Weapon(type='Broadsword', abilities=[CHANGLING, DX])
        self.assertTrue(w.changling)
        self.assert_('primaryweapon' in dir(w))
        self.assert_('secondaryweapon' in dir(w))
        self.assertTrue(isinstance(w.primaryweapon, Weapon))
        self.assertTrue(isinstance(w.secondaryweapon, Weapon))
        self.assertEqual(w.primaryweapon.type, 'Broadsword')
        self.assertEqual(w.primaryweapon.abilities, [DX,])
        self.assert_('Bow' in w.secondaryweapon.style)
        self.assert_(CHANGLING not in w.secondaryweapon.abilities)
        self.assertTrue(w.itemtype.startswith('Changling Broadsword /'))

        # Test with primary as missile weapon
        w = Weapon(type='Arbalest', abilities=[CHANGLING, DX])
        self.assertTrue(w.changling)
        self.assert_('primaryweapon' in dir(w))
        self.assert_('secondaryweapon' in dir(w))
        self.assertTrue(isinstance(w.primaryweapon, Weapon))
        self.assertTrue(isinstance(w.secondaryweapon, Weapon))
        self.assertEqual(w.primaryweapon.type, 'Arbalest')
        self.assertEqual(w.primaryweapon.abilities, [DX,])
        self.assert_('Bow' not in w.secondaryweapon.style)
        self.assert_(CHANGLING not in w.secondaryweapon.abilities)
        self.assertTrue(w.itemtype.startswith('Changling Arbalest /'))

        # Test specifying both
        s = Weapon(type='Arbalest', abilities=[CHANGLING, DX], secondary=True)
        w = Weapon(type='Broadsword', abilities=[CHANGLING, ST],
                   secondaryweapon=s)
        self.assertTrue(w.changling)
        self.assertFalse(w.secondaryweapon.changling)
        self.assertEqual(w.secondaryweapon.type, 'Arbalest')
        self.assertEqual(w.primaryweapon.type, 'Broadsword')
        self.assertEqual(w.secondaryweapon.abilities, [DX])
        self.assertEqual(w.primaryweapon.abilities, [ST])
        self.assertEqual(w.abilities, [ST, CHANGLING, DX])
        

    # Moved to StockItem:
    #def testshort(self):
    #    """(Special) should appear in .short() iff any WeaponAblities."""
    #    for i in range(100):
    #        w = Weapon()
    #        for ability in w.abilities:
    #            if isinstance(ability, WeaponAbility):
    #                self.assert_('(Special)' in w.short())
    #                break
    #        else:
    #            self.assert_('(Special)' not in w.short())

    def testrandom(self):
        """Ensure random weapons may be generated without error."""
        for i in range(100):
            Weapon()


class TestArmor(unittest.TestCase):

    def testarmortypes(self):
        """Create each type of armor, to ensure no errors occur."""
        for type in Armor.armortypes:
            a = Armor(type)
            self.assertEqual(a.type, type)
            self.assertIsNot(a.wearer, None)

    def testshieldtypes(self):
        """Create each type of shield, to ensure no errors occur."""
        for type in Armor.shieldtypes:
            a = Armor(type)
            self.assertEqual(a.type, type)
            self.assertIs(a.wearer, None)
                          
    def testinvalidtype(self):
        """Specify an invalid type, to generate an error."""
        self.assertRaises(ItemError, Armor, 'Invalid')
        self.assertRaises(ItemError, Armor, '')

    def testwearer(self):
        """Create each type of wearer, to ensure no errors occur."""
        for wearer in Armor.wearers:
            a = Armor(wearer=wearer)
            self.assertIn(a.type, Armor.armortypes)
            self.assertEqual(a.wearer, wearer)
            if wearer == 'Mount':
                self.assertIn(wearer, str(a))

    def testinvalidwearer(self):
        """Specify an invalid wearer, to generate an error."""
        self.assertRaises(ItemError, Armor, wearer='Invalid')
        self.assertRaises(ItemError, Armor, wearer='')
        self.assertRaises(ItemError, Armor, type='Tower Shield',
                                            wearer='Mount')

    def testabilities(self):
        """Exercise the specification of abilities."""
        for attr in Armor.attributes:
            abil = AttributeAbility(attr)
            a = Armor(abilities=[abil,])
            self.assertEqual(a.value, abil.AC)
        ST = AttributeAbility('ST')
        a = Armor(abilities=[ST, ST, ST, ST, ST])
        self.assertEqual(a.abilities, [ST, ST, ST, ST, ST])
        self.assertEqual(a.value, ST.AC * (1 + 2 + 4 + 8 + 16))

    def testinvalidabilities(self):
        """Provide invalid armor abilities, to generate errors."""
        self.assertRaises(ArtifactError, Armor, abilities=[])
        list = [AttributeAbility('ST'),] * 6
        self.assertRaises(ArtifactError, Armor, abilities=list)
        self.assertRaises(ArtifactError,
                          Armor, abilities=[AmuletAbility(),])
        self.assertRaises(ArtifactError, 
                          Armor, abilities=[MentalAbility(),])
        self.assertRaises(ArtifactError, 
                          Armor, abilities=[WeaponAbility(),])

    def testrandom(self):
        """Ensure random armor may be generated without error."""
        for i in range(100):
            Armor()


if __name__ == '__main__':
    unittest.main()









