try:
    import unittest2 as unittest
except ImportError:
    import unittest

from datatree.symbols import Symbol

tester = Symbol('tester')

class test_Symbol(unittest.TestCase):

    def test_one_level(self):
        self.assertEqual(tester.test, tester.test)
        self.assertIs(tester.test, tester.test)

    def test_nested(self):
        self.assertEqual(tester.test.real, tester.test.real)
        self.assertIs(tester.test.real, tester.test.real)
        self.assertFalse(tester.real is tester.test.real, 'Nested should not equal not nested.')

    def test_to_str(self):
        self.assertEqual(str(tester.testme), 'testme')

    def test_to_str_nested(self):
        self.assertEqual(str(tester.testme.testme), 'testme')
        
    def test_accessor_special_char_str(self):
        self.assertEqual(str(tester['A Name']), 'A Name')
        self.assertEqual(str(tester['A Name!']), 'A Name!')
        
    def test_accessor_special_char(self):
        self.assertIs(tester['Another Name'], tester['Another Name'])

    def test_accessor_special_char_nested(self):
        self.assertIs(tester["Root Node"]["Nested One"], tester["Root Node"]["Nested One"])
        
    def test_accessor(self):
        self.assertIsNotNone(tester["Who Has?"])