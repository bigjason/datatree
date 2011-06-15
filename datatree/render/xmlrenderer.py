from xml.sax.saxutils import escape, quoteattr
from StringIO import StringIO # cStringIO has no unicode support. Do we care?

from datatree.render.base import InternalRenderer
from datatree.node import Tree, CDataNode, CommentNode, DeclarationNode, InstructionNode
from datatree.symbols import Symbol

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
        indent = options.get('indent') * level if options.get('pretty') else ''
        newline = '\n' if options.get('pretty') else ''

        def safe_str(val):
            return str(val) if val != None else ''

        def safe_quote(val):
            return val.replace('"', '&quot;')

        def start_line_str():
            return "{}{}".format(newline, indent)

        def start_line():
            doc.write(start_line_str())

        def render_children():
            for child in node.__children__:
                self.render_node(child, doc=doc, level=level + 1, options=options)

        def data_node():
            attrs = self.get_attrs_str(node.__attrs__)
            if not node.__children__ and node.__value__ == None:
                doc.write('<{} {}{}/>'.format(node.__node_name__,
                                              attrs,
                                              ' ' if attrs else ''))
            else:
                doc.write('<{}{}{}>'.format(node.__node_name__,
                                            ' ' if attrs else '',
                                            attrs))
                if node.__value__ != None:
                    if len(node.__children__) > 0:
                        doc.write(newline)
                        doc.write(indent)
                    doc.write(escape(str(node.__value__)))

                render_children()

                if len(node.__children__) > 0:
                    doc.write(newline)
                    doc.write(indent)
                doc.write('</{}>'.format(node.__node_name__))

        def comment_node():
            doc.write('<!-- {} -->'.format(safe_str(node.__value__).strip()))

        def instruct_node():
            attrs = {}
            if node.__node_name__ == 'xml':
                attrs['version'] = '1.0'
                attrs['encoding'] = 'UTF-8'
            attrs.update(node.__attrs__)
            attrs_str = self.get_attrs_str(attrs)

            doc.write('<?{}{}{}?>'.format(node.__node_name__,
                                          ' ' if attrs_str else '',
                                          attrs_str))

        def declare_node():
            # Don't use standard attrib render.
            attrs = []
            for a in node.__declaration_params__:
                if isinstance(a, Symbol):
                    attrs.append(str(a))
                else:
                    attrs.append('"{}"'.format(safe_quote(safe_str(a))))
            if attrs:
                attrs_str = ' ' + ' '.join(attrs)
            else:
                attrs_str = ''

            doc.write('<!{}{}>'.format(node.__node_name__, attrs_str))

        def cdata_node():
            # Attrs are ignored for CDATA
            doc.write('<![CDATA[{}]]>'.format(safe_str(node.__value__)))

        ## Actual flow of render starts here ##

        if doc == None:
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
        attrs = ('{}={}'.format(key, quoteattr(str(value)))
                    for key, value in attrs.iteritems())
        return ' '.join(attrs).strip()
