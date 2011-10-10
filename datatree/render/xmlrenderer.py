"""
Outputs the tree as an xml string.  It is available under the alias ``'xml'``.

Options
-------

======= ============================================================== ===========
Name    Description                                                    Default
======= ============================================================== ===========
pretty  When True, Outputs the xml document with pretty formatting.    ``False``
indent  Used with pretty formatting.  It is the string that will       ``'    '``
        be used to indent each level.
======= ============================================================== ===========

Example Output
--------------
.. code-block:: python

    tree('xml', pretty=True)

Or even shorter:

.. code-block:: python

    tree(pretty=True)

.. code-block:: xml 

    <author>
        <name>Terry Pratchett</name>
        <genre>Fantasy/Comedy</genre>
        <!-- Only 2 books listed -->
        <novels count="2">
            <novel year="1992">Small Gods</novel>
            <novel year="1999">The Fifth Elephant</novel>
            <novel year="1989">Guards! Guards!</novel>
        </novels>
    </author>
"""
from xml.sax.saxutils import escape, quoteattr
from StringIO import StringIO # TODO: cStringIO has no unicode support. Do we care?

from datatree.render.base import InternalRenderer
from datatree.symbols import Symbol
from datatree.tree import (Tree,
                           CDataNode,
                           CommentNode,
                           DeclarationNode,
                           InstructionNode)

class XmlRenderer(InternalRenderer):
    """
    Custom xml provider to support full xml options.
    """
    default_options = {
        'pretty': False,
        'indent': '    '
    }

    def render_node(self, node, doc=None, options=None, level=0):
        options = self.get_options(options)
        if isinstance(node, Tree): level = -1
        indent = options['indent'] * level if options['pretty'] else ''
        newline = '\n' if options.get('pretty') else ''

        def safe_str(val):
            return str(val) if val is not None else ''

        def safe_quote(val):
            return val.replace('"', '&quot;')

        def start_line_str():
            return "{0}{1}".format(newline, indent)

        def start_line():
            if options['pretty'] and doc.len > 0:
                doc.write(start_line_str())

        def render_children():
            for child in node.__children__:
                self.render_node(child, doc=doc, level=level + 1,
                                 options=options)

        def data_node():
            attributes = self.get_attrs_str(node.__attributes__)
            if not node.__children__ and node.__value__ is None:
                doc.write('<{0} {1}{2}/>'.format(node.__node_name__,
                                                 attributes,
                                                 ' ' if attributes else ''))
            else:
                doc.write('<{0}{1}{2}>'.format(node.__node_name__,
                                               ' ' if attributes else '',
                                               attributes))
                if node.__value__ is not None:
                    if len(node.__children__) > 0:
                        doc.write(newline)
                        doc.write(indent)
                    doc.write(escape(str(node.__value__)))

                render_children()

                if len(node.__children__) > 0:
                    doc.write(newline)
                    doc.write(indent)
                doc.write('</{0}>'.format(node.__node_name__))

        def comment_node():
            doc.write('<!-- {0} -->'.format(safe_str(node.__value__).strip()))

        def instruct_node():
            attrs = {}
            if node.__node_name__ == 'xml':
                attrs['version'] = '1.0'
                attrs['encoding'] = 'UTF-8'
            attrs.update(node.__attributes__)
            attrs_str = self.get_attrs_str(attrs)

            doc.write('<?{0}{1}{2}?>'.format(node.__node_name__,
                                             ' ' if attrs_str else '',
                                             attrs_str))

        def declare_node():
            # Don't use standard attrib render.
            attrs = []
            for a in node.__declaration_params__:
                if isinstance(a, Symbol):
                    attrs.append(str(a))
                else:
                    attrs.append('"{0}"'.format(safe_quote(safe_str(a))))
            if attrs:
                attrs_str = ' ' + ' '.join(attrs)
            else:
                attrs_str = ''

            doc.write('<!{0}{1}>'.format(node.__node_name__, attrs_str))

        def cdata_node():
            # Attrs are ignored for cdata
            doc.write('<![cdata[{0}]]>'.format(safe_str(node.__value__)))

        ## Actual flow of render starts here ##

        if doc is None:
            doc = StringIO()

        if isinstance(node, Tree):
            render_children()
        elif isinstance(node, CommentNode):
            start_line()
            comment_node()
        elif isinstance(node, InstructionNode):
            start_line()
            instruct_node()
        elif isinstance(node, DeclarationNode):
            start_line()
            declare_node()
        elif isinstance(node, CDataNode):
            start_line()
            cdata_node()
        else:
            start_line()
            data_node()

        return doc.getvalue()

    def render_final(self, rendered, options=None):
        return rendered

    @staticmethod
    def get_attrs_str(attrs):
        attrs = ('{0}={1}'.format(key, quoteattr(str(value)))
        for key, value in attrs.iteritems())
        return ' '.join(attrs).strip()
