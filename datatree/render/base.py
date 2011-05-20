

class Renderer(object):
    @property
    def friendly_names(self):
        raise NotImplementedError()

    def render_node(self, node):
        raise NotImplementedError()

    def render_final(self, rendered):
        raise NotImplementedError()

    def render_string(self, base_node):
        """Renders the entire tree under base_node as a string."""
        return self.render_final(self.render_node(base_node))

class InternalRenderer(Renderer):
    friendly_names = []