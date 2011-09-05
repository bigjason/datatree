try:
    import unittest2 as unittest
except ImportError:
    import unittest

from datatree import Tree
from datatree.tests.base import NodeTestBase
from datatree.render.dictrender import DictRenderer, NodeLossError

class test_DictRenderer(unittest.TestCase, NodeTestBase):
    def test_nested_render(self):
        self.assertDictEqual(
            self.get_dirty_tree().render('dict'),
            self.get_dirty_dict()
        )

    def test_flat_render(self):
        self.assertDictEqual(
            self.get_flat_tree()('dict'),
            self.get_flat_dict()
        )

    def test_children_distinct_names(self):
        tree = Tree()
        with tree.node('tree') as root:
            root.node('person', 'One')
            root.node('person', 'Two')
            root.node('person', 'Three')

        render = DictRenderer()
        self.assertSetEqual(
            render._children_distinct_names(root.__children__),
            set(["person"])
        )

    def test_children_distinct_names_are_different(self):
        tree = Tree()
        with tree.node('root') as root:
            root.node('person', 'One')
            root.node('different', 'Two')
            root.node('strokes', 'Three')
        render = DictRenderer()
        self.assertSetEqual(
            render._children_distinct_names(root.__children__),
            set(["person", "different", "strokes"])
        )

    def test_duplicate_nodes_conversion(self):
        self.assertDictEqual(
            self.get_unified_tree()('dict'),
            self.get_unified_dict()
        )

    def get_lossy_tree(self):
        tree = Tree()
        with tree.node('root', 'tale') as root:
            root.node('level', 'absurd')
            root.node('level', 'stupid')
            root.node('handle', 'lame')
        return tree

    def test_duplicate_nodes_nodelosserror(self):
        with self.assertRaises(NodeLossError):
            self.get_lossy_tree()('dict')

    def test_render_option_allow_node_loss(self):
        self.assertDictEqual(
            self.get_lossy_tree()('dict', allow_node_loss=True),
                {
                'root': {
                    'level': 'stupid',
                    'handle': 'lame'
                }
            }
        )

    def test_add_node_return(self):
        tree = Tree()
        root = tree.node('root')
        self.assertEqual(root, tree.__children__[0])

    def test_run_as_callable(self):
        tree = Tree()

        with tree.node('root') as root:
            root.node('item', 1)

        actual = tree('dict')
        expected = {'root': {'item': 1}}
        self.assertDictEqual(actual, expected)
