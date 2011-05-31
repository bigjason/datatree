import unittest
try:
    import xml.etree.cElementTree as e
except ImportError:
    import xml.etree.ElementTree as e

from datatree.node import Node

class test_ETreeRenderer(unittest.TestCase):
    def test_single_level(self):
        root = Node('a', 'Here', href='url', title='A Title')
        actual = root.render('xml')
        result = e.fromstring(actual)

        self.assertEqual(result.tag, 'a')
        self.assertEqual(result.attrib['href'], 'url')
        self.assertEqual(result.attrib['title'], 'A Title')
        self.assertEqual(result.text, 'Here')

    def test_multi_level(self):
        root = Node('root', level=1)
        with root.second(level=2) as two:
            two.third('Three', level=3)
        root.fourth('four', level=2)

        actual = root.render('xml')

        # Parse the xml and break it into pieces to assert.
        result = e.fromstring(actual)
        second = result.find('second')
        third = result.find('.//third')
        fourth = result.find('fourth')

        self.assertEqual(result.tag, 'root')
        self.assertEqual(result.attrib['level'], '1')
        self.assertEqual(second.attrib['level'], '2')
        self.assertEqual(third.text, 'Three')
        self.assertEqual(third.attrib['level'], '3')
        self.assertEqual(fourth.text, 'four')
        self.assertEqual(fourth.attrib['level'], '2')
