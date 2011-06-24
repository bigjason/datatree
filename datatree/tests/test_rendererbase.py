try:
    import unittest2 as unittest
except ImportError:
    import unittest

from datatree.render.base import Renderer, InternalRenderer
from datatree import Tree

class test_Renderer(unittest.TestCase):

    def test_friendly_names_error(self):
        with self.assertRaises(NotImplementedError):
            self.assertListEqual(Renderer().friendly_names, [])

    def test_friendly_names_ok(self):
        class Tester(Renderer):
            friendly_names = ['A']
            
        self.assertListEqual(Tester().friendly_names, ['A'])
        
    def test_required_methods(self):
        r = Renderer()
        with self.assertRaises(NotImplementedError):
            r.friendly_names()
        with self.assertRaises(NotImplementedError):
            r.render_node(None)
        with self.assertRaises(NotImplementedError):
            r.render_final(None)
        with self.assertRaises(NotImplementedError):
            r.render_native(None)

class test_InternalRenderer(unittest.TestCase):
    
    def test_default_options_not_implemented(self):
        r = InternalRenderer()
        with self.assertRaises(NotImplementedError):
            r.default_options

    def _get_test_tree(self):
        tree = Tree()
        tree.INSTRUCT()
        tree.name('Bob')
        tree.age(12)
        return tree
            
    def test_data_only(self):
        actual = len(InternalRenderer().data_only(self._get_test_tree()))
        self.assertEqual(actual, 2)
        
    def test_instruction_only(self):
        actual = len(InternalRenderer().instruction_only(self._get_test_tree()))
        self.assertEqual(actual, 1)
