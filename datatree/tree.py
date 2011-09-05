from StringIO import StringIO

from .symbols import Symbol
from .utils import get_class

__all__ = ['Tree', 'Node', 'n', 'Name', '__']

Name = Symbol('Name')
__ = Name

_plugins = [
    [("xml",), 'datatree.render.xmlrenderer.XmlRenderer'],
    [('dict', 'dictionary'), 'datatree.render.dictrender.DictRenderer'],
    [('json', 'jsn', 'js'), 'datatree.render.jsonrender.JsonRenderer'],
    [('yaml', 'yml'), 'datatree.render.yamlrender.YamlRenderer']
]

class BaseNode(object):
    def __init__(self, node_name='root', node_value=None, node_parent=None,
                 node_namespace=None, **attributes):
        """

        :param node_name: The name identifier for the node.  Default value is
            ``'root'``.
        :param node_value: The value of this node.  Note that this will be
            converted to a string usually during rendering.  Default is ``None``
            which generally means it is ignored during rendering.
        :param node_parent: The parent node if any.
        :param node_namespace: The declared namespace for the ``Node``.  A dict
        :param attributes:
        """
        self.__children__ = []
        self.__node_name__ = node_name
        self.__value__ = node_value
        self.__parent__ = node_parent
        self.__name_space__ = node_namespace
        self.__attributes__ = attributes

    @staticmethod
    def register_renderer(klass):
        """Register a renderer class with the datatree rendering system.
        
        :keyword klass: Either a string with the fully qualified name of the 
          renderer class to register, or the actual class itself.  The name
          will be read from the class. 
        """
        if isinstance(klass, str):
            klass = get_class(klass)
        global _plugins
        _plugins.append([tuple(klass.friendly_names), klass])

    def __get_methods__(self):
        return set(['to_string', 'render', 'register_renderer'])

    def __str__(self):
        return '{0}/{1}'.format(self.__node_name__, self.__value__)

    def to_string(self, level=0):
        """Create an ugly representation of the datatree from this node
        down. This is included as a debug aid and is not good for much else.
        """
        result = StringIO()
        prefix = ' ' * level
        new_level = level + 2
        result.write(prefix)
        result.write(str(self))
        result.write('\n')
        for child in self.__children__:
            result.write(child.to_string(new_level))

        return result.getvalue()

    def render(self, renderer='xml', as_root=False, **options):
        """Render the datatree using the provided renderer.
        
        :keyword renderer: The name of the renderer to use.  You may add more
            renderers by using the register_renderer method.
            
        :keyword as_root: If True, the tree will be rendered from this node down,
            otherwise rendering will happen from the tree root.
        
        :keyword options: Key value pairs of options that will be passed to
            the renderer.         
        """
        if not as_root and self.__parent__:
            return self.__parent__.render(renderer, **options)

        global _plugins
        render_kls = None
        for plugin in _plugins:
            names, kls = plugin
            if renderer in names:
                if not isinstance(kls, str):
                    render_kls = kls
                else:
                    # Fetch the class and cache it for later.
                    render_kls = get_class(kls)
                    plugin[1] = render_kls
                break
                # TODO: Should the renderers be instantiated?
        return render_kls().render(self, options=options)

    def __call__(self, renderer='xml', **options):
        """Same as calling :function:`render <NodeBase.render>`.        
        """
        return self.render(renderer, **options)


class Vertex(BaseNode):
    """Node that can have children.
    """

    def __init__(self, *args, **kwargs):
        super(Vertex, self).__init__(*args, **kwargs)
        self.__methods__ = self.__get_methods__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def comment(self, text):
        """Adds a comment to the node.
        
        *Note: Comments are ignored by some of the renderers such as json and
            dict. Consult the documentation to find out the behaviour.*
        
        :keyword text: Text of the comment.
        """
        return self.add_node(
            CommentNode(
                node_name="!COMMENT!",
                node_value=text,
                node_parent=self
            )
        )

    def cdata(self, text, **attributes):
        return self.add_node(
            CDataNode(
                node_name='!CDATA!',
                node_value=text,
                **attributes
            )
        )

    def ns(self, name=None, url=None):
        ns = NameSpace(name_space=url)
        setattr(self, name, ns)
        return ns


    ### Child Manipulation Methods ###

    def node(self, name, text=None, **attributes):
        new_node = Node(
            node_name=name,
            node_value=text,
            **attributes
        )
        self.add_node(new_node)
        return new_node

    def add_node(self, node):
        self.__children__.append(node)
        return node


class Leaf(BaseNode):
    """Node that can have no children.
    """
    pass


class Tree(Vertex):
    """Very top node in a datatree.
    
    The Tree is the top node used to build a datatree.
    """

    def __init__(self, *args, **kwargs):
        kwargs['node_name'] = None
        super(Tree, self).__init__(*args, **kwargs)

    def instruct(self, name='xml', **attributes):
        """Add an xml processing instruction.
        
        :keyword name: Name of the instruction node. A value of xml will create 
            the instruction ``<?xml ?>``.
        
        :keyword attributes: Any extra attributes for the instruction.
        """
        return self.add_node(InstructionNode(node_name=name, **attributes))

    def declare(self, name, *attributes):
        """Add an xml declaration to the datatree.  
        
        *Note:* This functionality is pretty limited for the time being,
        hopefully the API for this will become more clear with time.
        
        :keyword name: Name of the declaration node.
        
        :keyword attrs: Extra attributes to be added. Strings will be added as 
            quoted strings.  Symbols will be added as unquoted strings. Import
            the ``__`` object and use it like this: ``__.SomeValue`` to add a
            symbol.
        """
        child = self.add_node(DeclarationNode(node_name=name))
        child.__declaration_params__ = attributes
        return child


class Node(Vertex):
    """A node is able to be instantiated directly and added to any Vertex.
    """

    def __init__(self, node_name='root', node_value=None, **attributes):
        super(Node, self).__init__(node_name=node_name, node_value=node_value,
                                   **attributes)


class InstructionNode(Leaf):
    pass


class DeclarationNode(Leaf):
    pass


class CommentNode(Leaf):
    def __str__(self):
        """Return a string representation.

        :return: A generic comment string.

        >>> cmt = CommentNode(node_value='A comment of some type.')
        >>> str(cmt)
        '# A comment of some type.'
        """
        return "# {0}".format(self.__value__)


class CDataNode(Leaf):
    pass


class NameSpace(Vertex):
    """A namespace is declared on the tree and accepts child nodes.  It is
    mostly ignored by the renderers with the exception of the XMLRenderer.
    """

    def __init__(self, *args, **kwargs):
        super(NameSpace, self).__init__(*args, **kwargs)