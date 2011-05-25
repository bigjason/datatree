import unittest

from datatree.node import Node, S
from datatree.render.dictrender import DictTreeRenderer, NodeLossError

class test_DictRenderer(unittest.TestCase):
    def test_nested_render(self):
        root = Node('root')
        root.name('Ponty Feeb')
        root.place('Holey')
        with root.books() as books:
            books.one(1)
            books.two(2)

        actual = root.render('dict')
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
        
    def test__children_distinct_names(self):
        root = Node()
        root.person('One')
        root.person('Two')
        root.person('Three')
        
        render = DictTreeRenderer()
        self.assertSetEqual(render._children_distinct_names(root.__children__), set(["person"]))

    def test__children_distinct_names_are_different(self):
        root = Node()
        root.person('One')
        root.different('Two')
        root.strokes('Three')
        
        render = DictTreeRenderer()
        expected = set(["person", "different", "strokes"])
        self.assertSetEqual(render._children_distinct_names(root.__children__), expected)
        
    def test__children_distinct_names_large(self):
        render = DictTreeRenderer()
        root = Node()

        root << [S('Node', i) for i in range(1000)]
        expected = set(["Node"])
        self.assertSetEqual(render._children_distinct_names(root.__children__), expected)
        
        root.different('I am different')
        expected.add('different')
        self.assertSetEqual(render._children_distinct_names(root.__children__), expected)
    

    def test_duplicate_nodes_conversion(self):
        root = Node('tale')
        root.level('absurd')
        with root.people() as people:
            people.person('Hobo')
            people.person('Princess')

        actual = root.render('dict')
        expected = {'tale': {
                'level': 'absurd',
                'people': ['Hobo', 'Princess']
            }
        }
        self.assertDictEqual(actual, expected)

    def test_duplicate_nodes_nodelosserror(self):
        root = Node('tale')
        root.level('absurd')
        root.level('stupid')
        root.handle('lame')
        
        with self.assertRaises(NodeLossError):
            root.render('dict')

    def test_render_option_allow_node_loss(self):
        root = Node('tale')
        root.level('absurd')
        root.level('stupid')
        root.handle('lame')
        
        actual = root.render('dict', allow_node_loss=True)
        expected = {'tale': {
                'level': 'stupid',
                'handle': 'lame'
            }
        }
        self.assertDictEqual(actual, expected)
        
    def test_default_root_name(self):
        root = Node()
        self.assertEqual(root.__node_name__, "root")

    def test_run_as_callable(self):
        root = Node()
        root.item(1)

        actual = root('dict')
        expected = {'root': {'item': 1}}
        self.assertDictEqual(actual, expected)
