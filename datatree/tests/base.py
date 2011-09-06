import logging

from datatree import Tree

logger = logging.getLogger(__name__)

class NodeTestBase(object):
    """
    Base class used to aid in testing.
    """

    def get_unified_tree(self):
        tree = Tree()
        with tree.node("author") as author:
            author.node('name', 'Terry Pratchett')
            author.node('genre', 'Fantasy/Comedy')
            with author.node('novels', count=2) as novels:
                novels.node('novel', 'Small Gods', year=1992)
                novels.node('novel', 'The Fifth Elephant', year=1999)
                novels.node('novel', 'Feet of Clay', year=1996)
        return tree

    def get_unified_dict(self):
        return {
            "author": {
                "name": 'Terry Pratchett',
                'genre': 'Fantasy/Comedy',
                'novels': [
                    'Small Gods',
                    'The Fifth Elephant',
                    'Feet of Clay'
                ]
            }
        }

    def get_dirty_tree(self):
        tree = Tree()
        with tree.node("author") as author:
            author.node('name', 'Terry Pratchett')
            with author.node('genre') as genre:
                genre.node('fantasy', 'true')
                genre.node('comedy', 'true')
                genre.node('horror', 'false')
        return tree

    def get_dirty_dict(self):
        return {
            "author": {
                "name": 'Terry Pratchett',
                'genre': {
                    'fantasy': 'true',
                    'comedy': 'true',
                    'horror': 'false'
                }
            }
        }

    def get_flat_tree(self):
        tree = Tree()
        with tree.node("author") as author:
            author.node('name', 'Terry Pratchett')
            author.node('genre', 'Fantasy/Comedy')
        return tree

    def get_flat_dict(self):
        return {
            "author": {
                "name": 'Terry Pratchett',
                'genre': 'Fantasy/Comedy',
                }
        }

    def test_tree_exists(self):
        assert self.get_dirty_tree() is not None
        assert self.get_unified_tree() is not None

