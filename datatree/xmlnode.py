from xml.dom import minidom
try:
    import xml.etree.cElementTree as e
except ImportError:
    import xml.etree.ElementTree as e

from .nodebase import NodeBase

class NodeXml(NodeBase):

    def __get_methods__(self):
        this = set(["to_xml_str", "to_etree", "to_xml"])
        other = super(NodeXml, self).__get_methods__()
        return other.union(this)


    def to_xml(self, parent=None):
        attrs = { key: str(value) for key, value in self.__attrs__.iteritems() }
        if parent is not None:
            root = e.SubElement(parent, self.__node_name__, attrs)
        else:
            root = e.Element(self.__node_name__ or "root", attrs)

        if self.__value__ is not None:
            root.text = str(self.__value__)

        for child in self.__children__:
            child.to_xml(root)

        return root
    
    def to_etree(self):
        return e.ElementTree(self.to_xml())
    
    def to_xml_str(self, pretty=True):
        return self.__pretty_xml__(e.tostring(self.to_xml()))

    @staticmethod
    def __pretty_xml__(xml_str, indent="  ", encoding=None):
        result = minidom.parseString(xml_str).toprettyxml(indent=indent, encoding=encoding)
        if encoding:
            result = unicode(result, encoding)
        return result
