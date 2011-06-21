"""
Outputs the tree as json string using the python json module.  It is available
under the alias ``'json'``, ``'jsn'`` or ``'js'``.

Options
-------

=========  =================================================
Name       Description
=========  =================================================
pretty     Outputs the json document with pretty formatting.
sort_keys  Sorts the keys in the json document. 
=========  =================================================

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

from .dictrender import DictTreeRenderer

class JsonRenderer(DictTreeRenderer):
    default_options = {
        'pretty': True,
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
        if options == None: options = {}
        used_options = self.get_options(options)
        kwargs = self._get_opts_kw(used_options)
        return dumps(self.render_final(self.render_node(base_node, options=used_options), options=used_options), **kwargs)
