from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

from .dictrender import DictTreeRenderer

class YamlRenderer(DictTreeRenderer):
    default_options = {
    }

    def render(self, base_node, options=None):
        """Renders the entire tree under base_node as a json string."""
        if options == None: options = {}
        return dump(self.render_final(self.render_node(base_node, options=options), options=options), Dumper=Dumper)
