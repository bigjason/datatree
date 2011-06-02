from xml.sax.saxutils import escape, quoteattr
from StringIO import StringIO # cStringIO has no unicode support. Do we care?

from datatree.render.base import InternalRenderer
from datatree.node import NodeType

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
        indent = options.get('indent') * level if options.get('pretty') else ''
        newline = '\n' if options.get('pretty') else ''

        def start_line_str():
            return "{}{}".format(newline, indent)

        def start_line():
            doc.write(start_line_str())

        def data_node():
            attrs = self.get_attrs_str(node.__attrs__)
            if not node.__children__ and not node.__value__:
                doc.write('<{} {}{}/>'.format(node.__node_name__,
                                              attrs,
                                              ' ' if attrs else ''))
            else:
                doc.write('<{}{}{}>'.format(node.__node_name__,
                                            ' ' if attrs else '',
                                            attrs))
                if node.__value__:
                    if len(node.__children__) > 0:
                        doc.write(newline)
                        doc.write(indent)
                    doc.write(escape(str(node.__value__)))

                for child in node.__children__:
                    self.render_node(child, doc=doc, level=level + 1, options=options)

                if len(node.__children__) > 0:
                    doc.write(newline)
                    doc.write(indent)
                doc.write('</{}>'.format(node.__node_name__))

        def comment_node():
            doc.write('<!-- {} -->'.format(str(node.__value__ or '').strip()))

        def instruct_node(child_node):
            attrs = {}
            if child_node.__node_name__ == 'xml':
                attrs['version'] = '1.0'
                attrs['encoding'] = 'UTF-8'
            attrs.update(child_node.__attrs__)
            attrs_str = self.get_attrs_str(attrs)

            return '<?{}{}{}?>'.format(child_node.__node_name__,
                                       ' ' if attrs_str else '',
                                       attrs_str)

        def declare_node():
            pass

        if doc is None:
            doc = StringIO()
            # Only process instructions on the root node and always at the start
            l = start_line_str().join([instruct_node(child)
                                       for child in self.instruction_only(node)])
            doc.write(l)

        if node.__node_type__ == NodeType.DATA:
            start_line()
            data_node()
        elif node.__node_type__ == NodeType.COMMENT:
            start_line()
            comment_node()
        elif node.__node_type__ == NodeType.INSTRUCT:
            pass # INSTRUCT nodes are handled earlier in the process.
        elif node.__node_type__ == NodeType.DECLARE:
            start_line()
            declare_node()
        else:
            start_line()
            data_node() # Unknown type, try the sanest thing

        return doc.getvalue()

    def render_final(self, rendered, options=None):
        return rendered

    @staticmethod
    def get_attrs_str(attrs):
        attrs = ('{}={}'.format(key, quoteattr(str(value)))
                    for key, value in attrs.iteritems())
        return ' '.join(attrs).strip()
