from xml.dom import minidom
try:
    import xml.etree.cElementTree as e
except ImportError:
    import xml.etree.ElementTree as e

from .base import InternalRenderer

class ETreeRenderer(InternalRenderer):
    def render_node(self, node, parent=None, options={}):
        attrs = { key: str(value) for key, value in node.__attrs__.iteritems() }
        if parent is not None:
            root = e.SubElement(parent, node.__node_name__, attrs)
        else:
            root = e.Element(node.__node_name__ or "root", attrs)

        if node.__value__ is not None:
            root.text = str(node.__value__)

        for child in node.__children__:
            self.render_node(child, root)

        return root

    def to_etree(self):
        return e.ElementTree(self.to_xml())

    def render_final(self, rendered, pretty=True, options={}):
        return e.tostring(rendered)

    @staticmethod
    def to_pretty_xml(xml_str, indent="  ", encoding=None):
        """Slow and messy.  Don't use in production."""
        result = minidom.parseString(xml_str).toprettyxml(indent=indent, encoding=encoding)
        if encoding:
            result = unicode(result, encoding)
        return result
