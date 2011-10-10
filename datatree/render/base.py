from copy import deepcopy

from datatree.tree import Vertex, InstructionNode

class Renderer(object):
    @property
    def friendly_names(self):
        raise NotImplementedError()

    def render_node(self, node, options={}):
        raise NotImplementedError()

    def render_final(self, rendered, options={}):
        raise NotImplementedError()

    def render_native(self, options={}):
        raise NotImplementedError('No render_native() method is provided for this renderer.')

    def render(self, base_node, options):
        """Renders the entire tree under base_node as a string."""
        return self.render_final(self.render_node(base_node, options=options), options=options)

class InternalRenderer(Renderer):
    """Base class for included renderers."""
    friendly_names = []

    ### Node Methods ###

    def data_only(self, node):
        """Return all DATA child nodes only."""
        return self.__filter(node, Vertex)

    def instruction_only(self, node):
        """Return all instruct child nodes only."""
        return self.__filter(node, InstructionNode)

    def __filter(self, node, node_type):
        return [x for x in node.__children__ if isinstance(x, node_type)]

    ### Option Methods ###

    @property
    def default_options(self):
        raise NotImplementedError()

    def get_options(self, user_options):
        if user_options is None: user_options = {}
        options = deepcopy(self.default_options)
        options.update(user_options)
        return options
