try:
    import unittest2 as unittest
except ImportError:
    import unittest

from datatree import Node, Tree

class test_Node(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_single_level(self):
        root = Node('a', 'Here', href='url', title='A Title')

        self.assertEqual(root.__node_name__, 'a')
        self.assertEqual(root.__attributes__['href'], 'url')
        self.assertEqual(root.__attributes__['title'], 'A Title')
        self.assertEqual(root.__value__, 'Here')

    def test_nested(self):
        root = Node('one')
        root.node('item1', 1)
        with root.node('nested1') as nested:
            nested.node('nested2', 'two')

        self.assertEqual(root.__node_name__, 'one')
        self.assertEqual(root.__children__[0].__value__, 1)
        self.assertEqual(root.__children__[1].__children__[0].__value__, 'two')

    def test_context_manager(self):
        root = Node()
        with root as actual:
            self.assertEqual(root, actual)

    def test_add_node(self):
        root = Node('level1', 'two', some='attr')
        root.add_node(root)

        child = root.__children__[0]
        self.assertEqual(child.__node_name__, 'level1')
        self.assertEqual(child.__value__, 'two')
        self.assertDictEqual(child.__attributes__, {'some': 'attr'})

    def test_add_child_node(self):
        tree = Tree()
        node = tree.node('A Value')
        self.assertEqual(tree.__children__[0], node)

    def test_add_duplicate_nodes(self):
        root = Node()
        root.node('greeting', 'Hello')
        root.node('greeting', 'Hi')

        hello = root.__children__[0]
        hi = root.__children__[1]

        self.assertEqual(hello.__value__, 'Hello')
        self.assertEqual(hi.__value__, 'Hi')
        for child in root.__children__:
            self.assertEqual(child.__node_name__, 'greeting')


    def test_callable_render(self):
        root = Node()
        root.node('item', 1)

        actual = str(root())
        self.assertIn("root", actual)
        self.assertIn("item", actual)
