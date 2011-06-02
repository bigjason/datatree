import unittest
try:
    import xml.etree.cElementTree as e
except ImportError:
    import xml.etree.ElementTree as e

from datatree import Node
from datatree.render.xmlrenderer import XmlRenderer

class test_XmlRenderer(unittest.TestCase):
    def test_get_attrs_str(self):
        input = {'age': '<b>300</b>', 'weight': 225}
        actual = XmlRenderer.get_attrs_str(input)

        self.assertIn('age=', actual)
        self.assertIn('&lt;b&gt;300&lt;/b&gt;"', actual,
                      "Age was not escaped properly")
        self.assertIn("weight=", actual)
        self.assertIn('"225"', actual,
                      "weight was not quoted properly")

    def get_author(self):        
        author = Node('author', rating="<b>5/6 Stars</b>")
        author.name('Terry Pratchett')
        author.genere('Fantasy/Comedy')
        author.country(abbreviation="UK")
        author.living()
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)
            with novels.shorts(count=2) as shorts:
                shorts.short("Short Story 1")
                shorts.short("Short Story 2")
        return author
            
    def test_render_multi_levels(self):
        author = self.get_author()
        actual = e.fromstring(author.render('xml'))
        
        self.assertEqual(actual.find('name').text, 'Terry Pratchett')
        self.assertEqual(actual.find('.//shorts').attrib['count'], '2')

