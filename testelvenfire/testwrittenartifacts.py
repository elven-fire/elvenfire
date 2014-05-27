import unittest
from elvenfire.artifacts.written import *
from elvenfire.artifacts import ArtifactError
from elvenfire.abilities.itemabilities import AmuletAbility
from elvenfire.abilities.charabilities import *


class TestScroll(unittest.TestCase):

    def testability(self):
        """Create a Scroll using each valid ability, to verify no errors occur."""
        for name in MentalAbilityWithOpposites.getabilities():
            r = Scroll(abilities=[MentalAbilityWithOpposites(name)])
            self.assertEqual(len(r.abilities), 1)

    def testabilities(self):
        """Create a Scroll with multiple abilities, to verify no errors occur."""
        list = []
        for i in range(5):
            list.append(MentalAbility())
            r = Scroll(abilities=list)
            self.assertEqual(len(r.abilities), i + 1)

    def testinvalidability(self):
        """Provide an invalid ability, to generate an error."""
        self.assertRaises(ArtifactError, Scroll, abilities=[])
        list = [MentalAbility()] * 6
        self.assertRaises(ArtifactError, Scroll, abilities=list)
        self.assertRaises(ArtifactError, Scroll, abilities=[PhysicalAbility()])

    def testlanguage(self):
        """Create a Scroll in each language to verify no errors occur."""
        for language in languages:
            s = Scroll(language=language)
            self.assertEqual(s.language, language)
            self.assert_(language in str(s))

    def testinvalidlanguage(self):
        """Provide an invalid language, to generate an error."""
        self.assertRaises(ArtifactError, Scroll, language='Invalid')
        self.assertRaises(ArtifactError, Scroll, language='')

    def testvalue(self):
        ability = MentalAbility('Aid', 1)
        r = Scroll(abilities=[ability]*5, language='Common')
        self.assertEqual(r.value, round(ability.AC * (1 + 2 + 4 + 8 + 16) / 20))

        list = [MentalAbility('Destroy Artifact', 1), MentalAbility('Aid', 1)]
        value = round((1000 * 1 + 500 * 2) / 20)
        for language in languages:
            r = Scroll(abilities=list, language=language)
            self.assertTrue(isinstance(r.value, int))
            if language == 'Common':
                self.assertEqual(r.value, value)
            elif language in rarelanguages:
                self.assertEqual(r.value, round(value * 0.75))
            else:
                self.assertEqual(r.value, round(value * 0.90))

    def testrandom(self):
        """Ensure that Scrolls can be randomly generated without errors."""
        for i in range(100):
            Scroll()


class TestBook(unittest.TestCase):

    def testability(self):
        """Create a Book using each valid ability, to verify no errors occur."""
        for name in PhysicalAbility.abilities.keys():
            r = Book(abilities=[PhysicalAbility(name)])
            self.assertEqual(len(r.abilities), 1)
        for name in MentalAbilityWithOpposites.getabilities():
            r = Book(abilities=[MentalAbilityWithOpposites(name)])
            self.assertEqual(len(r.abilities), 1)

    def testabilities(self):
        """Create a Book with multiple abilities, to verify no errors occur."""
        list = []
        for i in range(25):
            list.append(PhysicalOrMentalAbility())
            r = Book(abilities=list)
            self.assertEqual(r.abilities, list)

    def testinvalidability(self):
        """Provide an invalid ability, to generate an error."""
        self.assertRaises(ArtifactError, Book, abilities=[])
        list = [MentalAbility()] * 26
        self.assertRaises(ArtifactError, Book, abilities=list)
        self.assertRaises(ArtifactError, Book, abilities=[AmuletAbility()])

    def testlanguage(self):
        """Create a Book in each language to verify no errors occur."""
        for language in languages:
            s = Book(language=language)
            self.assertEqual(s.language, language)
            self.assert_(language in str(s))
            value = round(sum([a.AC for a in s.abilities]) / 10)
            if language == 'Common':
                self.assertEqual(s.value, value)
            elif language in rarelanguages:
                self.assertEqual(s.value, round(value * 0.75))
            else:
                self.assertEqual(s.value, round(value * 0.90))

    def testinvalidlanguage(self):
        """Provide an invalid language, to generate an error."""
        self.assertRaises(ArtifactError, Book, language='Invalid')
        self.assertRaises(ArtifactError, Book, language='')

    def testrandom(self):
        """Ensure that Books can be randomly generated without errors."""
        for i in range(100):
            Book()


if __name__ == '__main__':
    unittest.main()



