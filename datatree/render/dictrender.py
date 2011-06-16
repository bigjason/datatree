from pprint import pformat

from datatree.render.base import InternalRenderer
from datatree.node import Tree

class DictTreeRenderer(InternalRenderer):
    default_options = {
        'pretty_string': False,
        'allow_node_loss': False
    }

    def _children_distinct_names(self, children):
        return set([c.__node_name__ for c in children])

    # TODO: Figure out how to handle attributes here.
    def render_node(self, node, parent=None, options=None):
        if parent == None: parent = {}
        if options == None: options = {}
        user_options = self.get_options(options)
        children = self.data_only(node)

        if children:
            children_names = self._children_distinct_names(children)
            if len(children) > 1 and \
               len(children_names) == 1:
                value = []
            elif (len(children) > 1 and \
                  len(children_names) > 1 and \
                  len(children_names) != len(children)) and \
                  not user_options['allow_node_loss']:
                raise NodeLossError()
            else:
                value = {}
            for child in children:
                self.render_node(child, value, options=options)
        else:
            value = node.__value__

        if isinstance(node, Tree):
            parent = value
        elif isinstance(parent, dict):
            parent[node.__node_name__] = value
        else:
            parent.append(value)
        return parent

    def render_final(self, rendered, options=None):
        options = self.get_options(options)
        if options.get('pretty_string', False) == True:
            return pformat(rendered, width=80)
        else:
            return rendered

# TODO: Move this class to a more general location.
class NodeLossError(Exception):
    def __init__(self, msg='One or more nodes were lost due to duplicate keys.'):
        super(NodeLossError, self).__init__(msg)
