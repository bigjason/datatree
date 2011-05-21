
from .utils import get_class

_plugins = [
    [("etree", "xml"), "datatree.render.etreerender.ETreeRenderer"],
    [("dict", "dictionary"), "datatree.render.dictrender.DictTreeRenderer"]
]

class NodeBase(object):
    def __get_methods__(self):
        return set(["render", "register_renderer"])

    def render(self, renderer="xml"):
        """Render the datatree from this node down using the provided renderer.
        
        :keyword renderer: The name of the renderer to use.  You may add more
            renderers by using the register_renderer method.        
        """
        global _plugins
        render_kls = None
        for plugin in _plugins:
            names, kls = plugin
            if renderer in names:
                if not isinstance(kls, str):
                    render_kls = kls
                else:
                    # Fetch the class and cache it for later.
                    render_kls = get_class(kls)
                    plugin[1] = render_kls
                break
        # TODO: Should the renderers be instantiated?
        return render_kls().render_string(self)

    @staticmethod
    def register_renderer(klass):
        """Register a renderer class with the datatree rendering system.
        
        :keyword klass: Either a string with the fully qualified name of the 
          renderer class to load, or the actual class itself. 
        """
        if isinstance(klass, str):
            klass = get_class(klass)
        global _plugins
        _plugins.append([tuple(klass.friendly_names), klass])