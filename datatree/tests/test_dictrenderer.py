import unittest

from datatree import Tree, S
from datatree.render.dictrender import DictTreeRenderer, NodeLossError

class test_DictRenderer(unittest.TestCase):
    def test_nested_render(self):
        tree = Tree()
        with tree.root('root') as root:
            root.name('Ponty Feeb')
            root.place('Holey')
            with root.books() as books:
                books.one(1)
                books.two(2)

        actual = tree.render('dict')
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
        tree = Tree()
        with tree.root() as root:
            root.person('One')
            root.person('Two')
            root.person('Three')
        
        render = DictTreeRenderer()
        self.assertSetEqual(render._children_distinct_names(root.__children__), set(["person"]))

    def test__children_distinct_names_are_different(self):
        tree = Tree()
        with tree.root() as root:
            root.person('One')
            root.different('Two')
            root.strokes('Three')
        
        render = DictTreeRenderer()
        expected = set(["person", "different", "strokes"])
        self.assertSetEqual(render._children_distinct_names(root.__children__), expected)
        
    def test__children_distinct_names_large(self):
        render = DictTreeRenderer()
        tree = Tree()
        with tree.root() as root:
            root << [S('Node', i) for i in range(1000)]
            
        expected = set(["Node"])
        self.assertSetEqual(render._children_distinct_names(root.__children__), expected)
        
        root.different('I am different')
        expected.add('different')
        self.assertSetEqual(render._children_distinct_names(root.__children__), expected)
    

    def test_duplicate_nodes_conversion(self):
        tree = Tree()
        with tree.tale() as root:
            root.level('absurd')
            with root.people() as people:
                people.person('Hobo')
                people.person('Princess')

        actual = tree.render('dict')
        expected = {'tale': {
                'level': 'absurd',
                'people': ['Hobo', 'Princess']
            }
        }
        self.assertDictEqual(actual, expected)

    def test_duplicate_nodes_nodelosserror(self):
        tree = Tree()
        with tree.root('tale') as root:
            root.level('absurd')
            root.level('stupid')
            root.handle('lame')
        
        with self.assertRaises(NodeLossError):
            tree.render('dict')

    def test_render_option_allow_node_loss(self):
        tree = Tree()
        with tree.tale() as root:
            root.level('absurd')
            root.level('stupid')
            root.handle('lame')
        
        actual = tree.render('dict', allow_node_loss=True)
        expected = {'tale': {
                'level': 'stupid',
                'handle': 'lame'
            }
        }
        self.assertDictEqual(actual, expected)
        
    def test_add_node_return(self):
        tree = Tree()
        root = tree.root()
        self.assertEqual(root, tree.__children__[0])

    def test_run_as_callable(self):
        tree = Tree()
        with tree.root() as root:
            root.item(1)

        actual = tree('dict')
        expected = {'root': {'item': 1}}
        self.assertDictEqual(actual, expected)
