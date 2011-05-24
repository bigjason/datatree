import unittest

from datatree.node import Node

class test_DictRenderer(unittest.TestCase):
    def test_nested_render(self):
        root = Node("root")
        root.name("Ponty Feeb")
        root.place("Holey")
        with root.books() as books:
            books.one(1)
            books.two(2)

        actual = root.render("dict")
        expected = {'root': {
                        'name': 'Ponty Feeb',
                        'place': 'Holey',
                        'books': {
                            'two': 2,
                            'one': 1
                        },
                    }
        }
        self.assertDictEqual(actual, expected)

    @unittest.skip("Not yet implemented")
    def test_duplicate_nodes_conversion(self):
        root = Node("tale")
        root.level("absurd")
        with root.people() as people:
            people.person("Hobo")
            people.person("Princess")

        actual = root.render("dict")
        expected = {"tale": {
                "level": "absurd",
                "people": ["Hobo", "Princess"]
            }
        }
        self.assertDictEqual(actual, expected)
