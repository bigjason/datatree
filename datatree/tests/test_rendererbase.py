import unittest

from datatree.render import Renderer


class test_Renderer(unittest.TestCase):

    def test_friendly_names_error(self):
        with self.assertRaises(NotImplementedError):
            self.assertListEqual(Renderer().friendly_names, [])

    def test_friendly_names_ok(self):
        class Tester(Renderer):
            friendly_names = ['A']
            
        self.assertListEqual(Tester().friendly_names, ['A'])