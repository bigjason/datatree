from json import loads
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from datatree import Tree
from datatree.tests.base import NodeTestBase

class test_JsonRenderer(unittest.TestCase, NodeTestBase):
    def json_to_dict(self, json):
        return loads(json)

    def test_nested_render(self):
        self.assertDictEqual(
            self.json_to_dict(self.get_dirty_tree().render('json')),
            self.get_dirty_dict()
        )

    def test_flat_render(self):
        self.assertDictEqual(
            self.json_to_dict(self.get_flat_tree()('json')),
            self.get_flat_dict()
        )

    def test_nested_render_pretty(self):
        self.assertDictEqual(
            self.json_to_dict(self.get_dirty_tree().render('json', pretty=True)),
            self.get_dirty_dict()
        )