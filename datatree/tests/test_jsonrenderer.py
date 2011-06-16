from json import loads
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from datatree import Tree

class test_JsonRenderer(unittest.TestCase):
    def json_to_dict(self, json):
        return loads(json)

    def test_json_basic(self):
        root = Tree().root()
        root.delay(500)

        json = root.render('json')
        actual = self.json_to_dict(json)

        expected = {'root': {'delay': 500}}

        self.assertEqual(actual, expected)


    def test_json_nested(self):

        author = Tree().author()
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
