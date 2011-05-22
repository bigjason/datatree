from json import dumps

from .dictrender import DictTreeRenderer

class JsonRenderer(DictTreeRenderer):
    def render(self, base_node):
        """Renders the entire tree under base_node as a json string."""
        return dumps(self.render_final(self.render_node(base_node)))
