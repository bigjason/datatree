from datatree.render.base import InternalRenderer

class DictTreeRenderer(InternalRenderer):
    # TODO: Figure out how to handle attributes here.
    def render_node(self, node, parent=None, options=None):
        if parent == None: parent = {}
        if options == None: options = {}
        
        if node.__children__:
            value = {}
            for child in node.__children__:
                self.render_node(child, value, options=options)
        else:
            value = node.__value__
            
        parent[node.__node_name__] = value
        return parent

    def render_final(self, rendered, options={}):
        return rendered

