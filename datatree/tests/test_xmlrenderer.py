try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    import xml.etree.cElementTree as e
except ImportError:
    import xml.etree.ElementTree as e

from datatree import Tree, __
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
        tree = Tree()        
        with tree.node('author', rating="<b>5/6 Stars</b>") as author:
            author.node('name', 'Terry Pratchett')
            author.node('genere', 'Fantasy/Comedy')
            author.node('country', abbreviation="UK")
            author.node('living')
            with author.node('novels', count=2) as novels:
                novels.node('novel', 'Small Gods', year=1992)
                novels.node('novel', 'The Fifth Elephant', year=1999)
                with novels.node('shorts', count=2) as shorts:
                    shorts.node('short', "Short Story 1")
                    shorts.node('short', "Short Story 2")
        return tree
            
    def test_render_multi_levels(self):
        author = self.get_author()
        actual = e.fromstring(author.render('xml'))
        
        self.assertEqual(actual.find('name').text, 'Terry Pratchett')
        self.assertEqual(actual.find('.//shorts').attrib['count'], '2')

    def test_render_comment(self):
        tree = Tree()
        tree.node('root').comment("Something Here")
        self.assertIn('<!-- Something Here -->', tree('xml'))

    def test_render_cdata_string(self):
        tree = Tree()
        tree.node('root').cdata("Some Value")
        self.assertIn('<![cdata[Some Value]]>', tree('xml'))
        
    def test_render_cdata_not_string(self):
        int_val = 1234567891011121314151617181920
        tree = Tree()
        tree.node('root').cdata(int_val)
        self.assertIn('<![cdata[{0}]]>'.format(str(int_val)), tree('xml'))
        
    def test_render_declaration(self):
        tree = Tree()
        tree.declare('ELEMENT', __.Value, 'A value here.')
        self.assertIn(tree(), r'<!ELEMENT Value "A value here.">')

    def test_render_declaration_no_values(self):
        tree = Tree()
        tree.declare('ELEMENT')
        self.assertIn(tree(), r'<!ELEMENT>')

    def test_render_instruction_xml(self):
        tree = Tree()
        tree.instruct('xml')
        self.assertIn(tree(), '<?xml version="1.0" encoding="UTF-8"?>')
        
    def test_render_instruction(self):
        tree = Tree()
        tree.instruct('process', do="Good")
        self.assertIn(tree(), '<?process do="Good"?>')

    def _get_complex_structure(self):        
        tree = Tree()
        tree.instruct('xml')
        #tree.cdata(r"<b>I am some text.</b>")
        tree.declare('DOCTYPE', __.author, __.SYSTEM,  'SomeDTD.dtd')
        with tree.node('author') as author:
            author.node('name', 'Terry Pratchett')
            author.node('genre', 'Fantasy/Comedy')
            author.comment("Only 2 books listed")
            with author.node('novels', count=2) as novels:
                novels.node('novel', 'Small Gods', year=1992)
                novels.node('novel', 'The Fifth Elephant', year=1999)
        return tree

    def test_parse_complex_doc(self):
        tree = self._get_complex_structure()
        etree = e.fromstring(tree())
        self.assertEqual(etree.find('.//genre').text, 'Fantasy/Comedy')
        self.assertEqual(len(etree.findall('.//novel')), 2)
        
    def test_parse_complex_doc_pretty(self):
        tree = self._get_complex_structure()
        etree = e.fromstring(tree(pretty=True))
        self.assertEqual(etree.find('.//genre').text, 'Fantasy/Comedy')
        self.assertEqual(len(etree.findall('.//novel')), 2)

    def test_data_node_with_children_and_text(self):
        tree = Tree()
        with tree.node('a', 'A', href="http://bigjason.com") as a:
            a.node('b', "Link")
        self.assertEqual(
            tree(),
            '<a href="http://bigjason.com">A<b>Link</b></a>'
        )
