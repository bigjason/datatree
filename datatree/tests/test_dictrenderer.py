import unittest

from datatree.node import Node

class test_DictRenderer(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_nested_render(self):
        root = Node("root")
        root.name("Ponty Feeb")
        root.place("Holey")
        with root.books() as books:
            books.one(1)
            books.two(2)
            
        actual = root.render("dict")
        expected = { "root": {
                "name": "Ponty Feeb",
                "place": "Holey",
                "books" : {
                    "one": 1,
                    "two": 2
                }
            }
        }

        self.assertDictEqual(expected, actual)
