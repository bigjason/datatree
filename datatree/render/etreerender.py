"""
Outputs the tree as an elementtree.  It is available under the alias ``'etree'``.

**Note:** *This module is not fully implemented.  It supports the basic node
types, but not comments, declarations, instructions or cdata.*

Options
-------

=========  ================================================= ==========
Name       Description                                       Default
=========  ================================================= ==========
as_string  Outputs the document as a string instead of a     ``False``
           populated elementtree.
=========  ================================================= ==========

"""

try:
    import xml.etree.cElementTree as e
except ImportError:
    import xml.etree.ElementTree as e

from datatree.render.base import InternalRenderer

class ETreeRenderer(InternalRenderer):
    default_options = {
        'as_string': False
    }

    def render_node(self, node, parent=None, options={}):
        attrs = {}
        for key, value in node.__attrs__.iteritems():
            attrs[key] = str(value)
        if parent is not None:
            root = e.SubElement(parent, node.__node_name__, attrs)
        else:
            root = e.Element(node.__node_name__ or 'root', attrs)

        if node.__value__ is not None:
            root.text = str(node.__value__)

        for child in node.__children__:
            self.render_node(child, root)

        return root

    def to_etree(self):
        return e.ElementTree(self.to_xml())

    def render_final(self, rendered, options={}):
        options = self.get_options(options)
        if options['as_string']:
            return e.tostring(rendered)
        else:
            return e.ElementTree(rendered)

