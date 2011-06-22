from StringIO import StringIO

from .symbols import Symbol
from .utils import get_class

__all__ = ['Tree', 'Node', 'n', 'Name', '__']

Name = Symbol('Name')
__ = Name

_plugins = [
    [("xml",), 'datatree.render.xmlrenderer.XmlRenderer'],
    [('etree'), 'datatree.render.etreerender.ETreeRenderer'],
    [('dict', 'dictionary'), 'datatree.render.dictrender.DictTreeRenderer'],
    [('json', 'jsn', 'js'), 'datatree.render.jsonrender.JsonRenderer'],
    [('yaml', 'yml'), 'datatree.render.yamlrender.YamlRenderer']
]

class BaseNode(object):
    def __init__(self, node_name='root', node_value=None, node_parent=None, **attrs):
        self.__children__ = []
        self.__node_name__ = node_name
        self.__value__ = node_value
        self.__parent__ = node_parent
        self.__attrs__ = attrs

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
        """Create an ugly representation of the datatree from this node down. This
        is included as a debug aid and is not good for much else.
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


class Vertice(BaseNode):
    """Node that can have children.
    """
    def __init__(self, **kwargs):
        super(Vertice, self).__init__(**kwargs)
        self.__methods__ = self.__get_methods__()

    def __get_methods__(self):
        this = set(['add_child', 'add_child_node', 'COMMENT', 'CDATA'])
        other = super(Vertice, self).__get_methods__()
        return other.union(this)

    def __getattribute__(self, name):
        try:
            if (name.startswith('__') and name.endswith('__')) or \
                name in self.__methods__:
                val = super(Vertice, self).__getattribute__(name)
                return val
            else:
                raise ValueError()
        except:
            def add_node_child(self, node_value=None, node_name=None, **attrs):
                child_node = Node(node_name=node_name or name,
                                  node_value=node_value, node_parent=self, **attrs)
                self.__children__.append(child_node)
                return child_node

            return add_node_child.__get__(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def COMMENT(self, text):
        """Adds a comment to the node. Alternatively you can use the ``//`` operator
        to create comments like this: ``tree // "A comment in here"``.  With the 
        XmlRenderer this would produce the comment ``<!--A comment in here -->``. 
        
        *Note: Comments are ignored by some of the renderers such as json.  Consult
        the documentation to find out the behaviour.*
        
        :keyword text: Text of the comment.
        """
        return self.add_child(child_class=CommentNode, node_name='!COMMENT!', node_value=text)

    def CDATA(self, text):
        return self.add_child(child_class=CDataNode, node_name='!CDATA!', node_value=text)

    ### Child Manipulation Methods ###

    def add_child(self, child_class=None, *args, **kwargs):
        if child_class == None:
            child_class = Node
        kwargs['node_parent'] = self
        child = child_class(*args, **kwargs)
        self.__children__.append(child)
        return child

    def add_child_node(self, child_node):
        """For use when adding an existing Node."""
        self.__children__.append(child_node)
        return child_node

    ### Operator Overloads ###

    def __lshift__(self, other):
        if isinstance(other, BaseNode):
            other = [other]
        for item in other:
            self.add_child_node(item)
        return self

    def __floordiv__(self, text):
        return self.COMMENT(text)

class Leaf(BaseNode):
    """Node that can have no children.
    """
    pass

class Tree(Vertice):
    """Very top node in a datatree.
    
    The Tree is the top node used to build a datatree.
    """
    def __init__(self, *args, **kwargs):
        kwargs['node_name'] = None
        super(Tree, self).__init__(*args, **kwargs)

    def __get_methods__(self):
        this = set(['DECLARE', 'INSTRUCT'])
        other = super(Tree, self).__get_methods__()
        return other.union(this)

    def INSTRUCT(self, name='xml', **attrs):
        """Add an xml processing instruction.
        
        :keyword name: Name of the instruction node. A value of xml will create 
            the instruction ``<?xml ?>``.
        
        :keyword attrs: Any extra attributes for the instruction. 
        """
        return self.add_child(child_class=InstructionNode, node_name=name, **attrs)

    def DECLARE(self, name, *attrs):
        """Add an xml declaration to the datatree.  
        *Note:* This functionality is pretty limited for the time being, hopefully
        the API for this will become more clear with time. 
        
        :keyword name: Name of the declaration node.
        
        :keyword attrs: Extra attributes to be added. Strings will be added as 
            quoted strings.  Symbols will be added as unquoted strings. Import
            the ``__`` object and use it like this: ``__.SomeValue`` to add a
            symbol.
        """
        child = self.add_child(child_class=DeclarationNode, node_name=name)
        child.__declaration_params__ = attrs
        return child

class Node(Vertice):
    def __init__(self, node_name='root', node_value=None, **attrs):
        super(Node, self).__init__(node_name=node_name, node_value=node_value, **attrs)
n = Node

class InstructionNode(Leaf):
    pass

class DeclarationNode(Leaf):
    pass

class CommentNode(Leaf):
    """
    >>> cmt = CommentNode(node_value='A comment of some type.')
    >>> str(cmt)
    '# A comment of some type.'    
    """
    def __str__(self):
        return "# {0}".format(self.__value__)

class CDataNode(Leaf):
    pass

