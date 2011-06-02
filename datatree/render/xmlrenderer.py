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
        attrs = self.get_attrs_str(node.__attrs__)

        def data_node():
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
            
        def instruct_node():
            pass
        
        def declare_node():
            pass

        if doc is None:
            doc = StringIO()
        else:
            doc.write(newline)
            doc.write(indent)

        if node.__node_type__ == NodeType.DATA:
            data_node()
        elif node.__node_type__ == NodeType.COMMENT:
            comment_node()
        elif node.__node_type__ == NodeType.INSTRUCT:
            instruct_node()
        elif node.__node_type__ == NodeType.DECLARE:
            declare_node()
        else:
            data_node() # Unknown type, try the sanest thing

        return doc.getvalue()

    def render_final(self, rendered, options=None):
        return rendered

    @staticmethod
    def get_attrs_str(attrs):
        attrs = ('{}={}'.format(key, quoteattr(str(value)))
                    for key, value in attrs.iteritems())
        return ' '.join(attrs).strip()
