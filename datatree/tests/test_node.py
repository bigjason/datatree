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


    def test_Edges(self):
        pass


if __name__ == "__main__":
    import sys
    sys.argv = ['', '-v 2']
    unittest.main()
