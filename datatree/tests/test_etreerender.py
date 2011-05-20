import unittest

from ..node import Node

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_single_level(self):
        root = Node("a", "Here", href="url", title="A Title")
        result = root.to_xml()
        
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.attrib["href"], "url")        
        self.assertEqual(result.attrib["title"], "A Title")
        self.assertEqual(result.text, "Here")
