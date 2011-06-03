import unittest

from datatree.node import Tree, NodeType

class test_Tree(unittest.TestCase):
    def test_tree_node_type(self):
        actual = Tree()
        self.assertEqual(actual.__node_type__, NodeType.TREE)
        
    def test_tree_node_type_with_children(self):
        actual = Tree()        
        with actual.html() as html:
            html.b("I am bold")
        self.assertEqual(actual.__node_type__, NodeType.TREE)
        
