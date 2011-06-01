from xml.sax.saxutils import escape, quoteattr
from StringIO import StringIO # cStringIO has no unicode support. Do we care?

from datatree.render.base import InternalRenderer

class XmlRenderer(InternalRenderer):
    """
    Custom xml provider to support full xml options.
    """
    
    default_options = {
        'pretty': False
    }

    def render_node(self, node, doc=None, options=None, level=0):
        options = self.get_options(options)
        indent = '    ' * level if options.get('pretty') else ''
        newline = '\n' if options.get('pretty') else ''
        
        attrs = self._get_attrs_str(node.__attrs__)
        if doc is None:
            doc = StringIO()
        else:
            doc.write(newline)
            doc.write(indent)

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

        return doc.getvalue()

    def render_final(self, rendered, options=None):
        return rendered

    @staticmethod
    def _get_attrs_str(attrs):
        attrs = ('{}={}'.format(key, quoteattr(str(value)))
                    for key, value in attrs.iteritems())
        return ' '.join(attrs).strip()
