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


    def _get_complex_tree(self):
        tree = Tree()
        author = tree.author()
        author.name('Terry Pratchett')
        author.genere('Fantasy/Comedy')
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)
        return tree

    _complex_expected = {'author': {
                          'name': 'Terry Pratchett',
                          'genere': 'Fantasy/Comedy',
                          'novels': ['Small Gods', 'The Fifth Elephant']
                          }
                        }

    def test_json_nested(self):
        author = self._get_complex_tree()
        actual = self.json_to_dict(author.render('json'))
        
        self.assertDictEqual(actual, self._complex_expected)

    def test_json_pretty(self):
        author = self._get_complex_tree()
        actual = self.json_to_dict(author.render('json', pretty=True))
        
        self.assertDictEqual(actual, self._complex_expected)
