import unittest

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
    
from datatree.node import Node

class test_YamlRenderer(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def yaml_to_dict(self, yaml_text):
        return load(yaml_text, Loader=Loader)
    
    def test_yaml_basic(self):
        root = Node('root')
        root.delay(500)

        json = root.render('yaml')
        actual = self.yaml_to_dict(json)

        expected = {'root': {'delay': 500}}

        self.assertEqual(actual, expected)


    def test_yaml_nested(self):

        author = Node('author')
        author.name('Terry Pratchett')
        author.genere('Fantasy/Comedy')
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)

        actual = self.yaml_to_dict(author.render('yaml'))
        expected = {'author': {
                        'name': 'Terry Pratchett',
                        'genere': 'Fantasy/Comedy',
                        'novels': ['Small Gods', 'The Fifth Elephant']
                    }
        }
        self.assertDictEqual(actual, expected)
