from StringIO import StringIO

from datatree.base import NodeBase

__all__ = ['Node', 'SubNode', 'S']

class NodeType(object):
    DATA = 1
    COMMENT = 2
    DECLARE = 3
    INSTRUCT = 4

class Node(NodeBase):
    def __init__(self, node_name='root', node_value=None,
            node_type=NodeType.DATA, **attrs):
        self.__children__ = []
        self.__node_name__ = node_name
        self.__value__ = node_value
        self.__node_type__ = node_type
        self.__attrs__ = attrs
        self.__methods__ = self.__get_methods__()

    def __get_methods__(self):
        this = set(['to_string', 'add_child', 'COMMENT', 'DECLARE',
                    'INSTRUCT'])
        other = super(Node, self).__get_methods__()
        return other.union(this)

    def __getattribute__(self, name):
        try:
            if (name.startswith('__') and name.endswith('__')) or \
                name in self.__methods__:
                val = super(Node, self).__getattribute__(name)
                return val
            else:
                raise ValueError()
        except:
            def add_child(self, node_value=None, node_name=None, **attrs):
                child_node = Node(node_name=node_name or name,
                                  node_value=node_value, **attrs)
                self.__children__.append(child_node)
                return child_node

            return add_child.__get__(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def __str__(self):
        return '{}/{}'.format(self.__node_name__, self.__value__)

    def to_string(self, level=0):
        result = StringIO()
        prefix = ' ' * level
        new_level = level + 2
        result.write(prefix)
        result.write(str(self))
        result.write('\n')
        for child in self.__children__:
            result.write(child.to_string(new_level))

        return result.getvalue()

    ### Child Manipulation Methods ###

    def add_child(self, *args, **kwargs):
        child = Node(*args, **kwargs)
        self.__children__.append(child)
        return child

    def COMMENT(self, text):
        return self.add_child(node_name="!COMMENT!", node_value=text, node_type=NodeType.COMMENT)

    def DECLARE(self, name, *attrs):
        return self.add_child(node_name=name, node_type=NodeType.DECLARE, *attrs)

    def INSTRUCT(self, name, **attrs):
        return self.add_child(node_name=name, node_type=NodeType.INSTRUCT, **attrs)

    ### Operator Overloads ###

    def __lshift__(self, other):
        if isinstance(other, SubNode):
            other = [other]
        for item in other:
            self.add_child(*item.args, **item.kwargs)
        return self

    def __floordiv__(self, text):
        return self.COMMENT(text)

class SubNode(object):
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
S = SubNode
