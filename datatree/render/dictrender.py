from pprint import pformat

from datatree.render.base import InternalRenderer

class DictTreeRenderer(InternalRenderer):
    default_options = {
        'pretty_string': False,
        'allow_node_loss': False
    }
    
    def _children_distinct_names(self, children):
        return { c.__node_name__ for c in children }

    # TODO: Figure out how to handle attributes here.
    def render_node(self, node, parent=None, options=None):
        if parent == None: parent = {}
        if options == None: options = {}
        user_options = self.get_options(options)

        if node.__children__:
            children_names = self._children_distinct_names(node.__children__)
            if len(node.__children__) > 1 and \
               len(children_names) == 1:
                value = []
            elif (len(node.__children__) > 1 and \
                  len(children_names) > 1 and \
                  len(children_names) != len(node.__children__)) and \
                  not user_options["allow_node_loss"]:
                raise NodeLossError()
            else:
                value = {}
            for child in node.__children__:
                self.render_node(child, value, options=options)
        else:
            value = node.__value__

        if isinstance(parent, dict):
            parent[node.__node_name__] = value
        else:
            parent.append(value)
        return parent

    def render_final(self, rendered, options=None):
        if options == None: options = {}
        user_options = self.get_options(options)
        if user_options.get("pretty_string", False) == True:
            return pformat(rendered, width=80)
        else:
            return rendered

# TODO: Move this class to a more general location.
class NodeLossError(Exception):
    def __init__(self, msg="One or more nodes were lost due to duplicate keys."):
        super(NodeLossError, self).__init__(msg)