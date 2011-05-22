from json import loads
import unittest

from datatree.node import Node

class test_JsonRenderer(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def json_to_dict(self, json):
        return loads(json)

    def test_json_basic(self):
        root = Node("root")
        root.delay(500)
        
        json = root.render("json")
        actual = self.json_to_dict(json)
        
        expected = {"root": {"delay": 500}}
        
        self.assertEqual(actual, expected)

