import unittest

from ..node import Node, S

class test_Node(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_single_level(self):
        root = Node("a", "Here", href="url", title="A Title")

        self.assertEqual(root.__node_name__, "a")
        self.assertEqual(root.__attrs__["href"], "url")
        self.assertEqual(root.__attrs__["title"], "A Title")
        self.assertEqual(root.__value__, "Here")

    def test_nested(self):
        root = Node("one")
        root.item1(1)
        with root.nested1() as nested:
            nested.nested2("two")

        self.assertEqual(root.__node_name__, "one")
        self.assertEqual(root.__children__[0].__value__, 1)
        self.assertEqual(root.__children__[1].__children__[0].__value__, "two")

    def test_context_manager(self):
        root = Node()
        with root as actual:
            self.assertEqual(root, actual, "The context manager should return itself.")

    def test_add_child(self):
        root = Node()
        root.add_child("level1", "two", some="attr")

        child = root.__children__[0]
        self.assertEqual(child.__node_name__, "level1")
        self.assertEqual(child.__value__, "two")
        self.assertDictEqual(child.__attrs__, {"some": "attr"})

    def test_lshift_operator_single(self):
        root = Node()
        root << S("level1", "two", some="attr")

        child = root.__children__[0]
        self.assertEqual(child.__node_name__, "level1")
        self.assertEqual(child.__value__, "two")
        self.assertDictEqual(child.__attrs__, {"some": "attr"})

    def test_lshift_operator_multi(self):
        root = Node()
        root << [S("level1", "two", some="attr"), S("level1", "two", some="attr")]

        for child in root.__children__:
            self.assertEqual(child.__node_name__, "level1")
            self.assertEqual(child.__value__, "two")
            self.assertDictEqual(child.__attrs__, {"some": "attr"})

    def test_lshift_operator_chained(self):
        root = Node()
        root << S("level1", "two", some="attr") << S("level1", "two", some="attr")

        for child in root.__children__:
            self.assertEqual(child.__node_name__, "level1")
            self.assertEqual(child.__value__, "two")
            self.assertDictEqual(child.__attrs__, {"some": "attr"})
