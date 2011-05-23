from .base import InternalRenderer

class DictTreeRenderer(InternalRenderer):
    def render_node(self, node, parent={}, options={}):
        # TODO: Figure out how to handle attributes here.
        if len(node.__children__) > 0:
            children = {}
            for child in node.__children__:
                self.render_node(child, children)
        else:
            children = node.__value__

        parent[node.__node_name__] = children
        return parent

    def render_final(self, rendered, options={}):
        return rendered

