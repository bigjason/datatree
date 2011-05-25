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
        root = Node('root')
        root.delay(500)

        json = root.render('json')
        actual = self.json_to_dict(json)

        expected = {'root': {'delay': 500}}

        self.assertEqual(actual, expected)


    def test_json_nested(self):

        author = Node('author')
        author.name('Terry Pratchett')
        author.genere('Fantasy/Comedy')
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)

        actual = self.json_to_dict(author.render('json'))
        expected = {'author': {
                        'name': 'Terry Pratchett',
                        'genere': 'Fantasy/Comedy',
                        'novels': ['Small Gods', 'The Fifth Elephant']
                    }
        }
        self.assertDictEqual(actual, expected)
