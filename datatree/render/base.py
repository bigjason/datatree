

class Renderer(object):
    @property
    def friendly_names(self):
        raise NotImplementedError()

    def render_node(self, node, options={}):
        raise NotImplementedError()

    def render_final(self, rendered, options={}):
        raise NotImplementedError()

    def render_native(self, options={}):
        raise NotImplementedError("No render_native() method is provided for this renderer.")

    def render(self, base_node, options):
        """Renders the entire tree under base_node as a string."""
        return self.render_final(self.render_node(base_node, options=options), options=options)

class InternalRenderer(Renderer):
    friendly_names = []
