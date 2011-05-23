from json import dumps

from .dictrender import DictTreeRenderer

class JsonRenderer(DictTreeRenderer):
    
    def _convert_options(self, options):
        default_options = {
            'pretty': True,
            'sort_keys': False
        }
        default_options.update(options)
        return default_options
    
    def _get_opts_kw(self, opts):
        result = {}
        if opts.get("pretty"):
            result["indent"] = 4
        result['sort_keys'] = opts.get('sort_keys')
        return result
    
    def render(self, base_node, options=None):
        """Renders the entire tree under base_node as a json string."""
        if options == None: options = {}
        used_options = self._convert_options(options)
        kwargs = self._get_opts_kw(used_options)
        return dumps(self.render_final(self.render_node(base_node, options=used_options), options=used_options), **kwargs)
