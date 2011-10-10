"""
Outputs the tree as json string using the python json module.  It is available
under the alias ``'json'``, ``'jsn'`` or ``'js'``.

Options
-------

=========  ================================================= ==========
Name       Description                                       Default
=========  ================================================= ==========
pretty     Outputs the json document with pretty formatting. ``False``
sort_keys  Sorts the keys in the json document.              ``False``
=========  ================================================= ==========

Example Output
--------------
.. code-block:: python

    tree('json', pretty=True)

.. code-block:: js 

    {
        "author": {
            "genre": "Fantasy/Comedy", 
            "name": "Terry Pratchett", 
            "novels": [
                "Small Gods", 
                "The Fifth Elephant", 
                "Guards! Guards!"
            ]
        }
    }
        
"""
from json import dumps

from .dictrender import DictRenderer

class JsonRenderer(DictRenderer):
    default_options = {
        'pretty': False,
        'sort_keys': False
    }

    def _get_opts_kw(self, opts):
        result = {}
        if opts.get('pretty'):
            result["indent"] = 4
        result['sort_keys'] = opts.get('sort_keys')
        return result

    def render(self, base_node, options=None):
        """Renders the entire tree under base_node as a json string."""
        if options is None: options = {}
        used_options = self.get_options(options)
        kwargs = self._get_opts_kw(used_options)
        return dumps(self.render_final(self.render_node(base_node, options=used_options), options=used_options), **kwargs)
