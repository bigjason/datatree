from StringIO import StringIO

from datatree.nodebase import NodeBase

__all__ = ["Node", "SubNode", "S"]

class Node(NodeBase):
    def __init__(self, node_name=None, node_value=None, **attrs):
        self.__children__ = []
        self.__node_name__ = node_name
        self.__value__ = node_value
        self.__attrs__ = attrs
        self.__methods__ = self.__get_methods__()

    def __get_methods__(self):
        this = set(["to_string", "add_child"])
        other = super(Node, self).__get_methods__()
        return other.union(this)

    def __getattribute__(self, name):
        try:
            if (name.startswith("__") and name.endswith("__")) or \
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
        return "{}/{}".format(self.__node_name__, self.__value__)

    def to_string(self, level=0):
        result = StringIO()
        prefix = " " * level
        new_level = level + 2
        # Write an indented self
        result.write(prefix)
        result.write(str(self))
        result.write("\n")
        # Write out each child
        for child in self.__children__:
            result.write(child.to_string(new_level))

        return result.getvalue()

    def add_child(self, *args, **kwargs):
        child = Node(*args, **kwargs)
        self.__children__.append(child)
        return child

    def __lshift__(self, other):
        if isinstance(other, SubNode):
            other = [other]
        for item in other:
            self.add_child(*item.args, **item.kwargs)
        return self

class SubNode(object):
    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
S = SubNode
