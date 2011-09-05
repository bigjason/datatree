try:
    import unittest2 as unittest
except ImportError:
    import unittest

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
    
from datatree import Tree
from datatree.tests.base import NodeTestBase

class test_YamlRenderer(unittest.TestCase, NodeTestBase):
    def yaml_to_dict(self, yaml_text):
        return load(yaml_text, Loader=Loader)

    def test_nested_render(self):
        self.assertDictEqual(
            self.yaml_to_dict(self.get_dirty_tree().render('yaml')),
            self.get_dirty_dict()
        )

    def test_flat_render(self):
        self.assertDictEqual(
            self.yaml_to_dict(self.get_flat_tree()('yaml')),
            self.get_flat_dict()
        )

