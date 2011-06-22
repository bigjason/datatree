"""
Outputs the tree as yaml string using the `PyYAML <http://pypi.python.org/pypi/PyYAML/>`_
package (which must be installed).  It is available under the alias ``'yaml'``
or ``'yml'``.

Options
-------

=========  ================================================= ===========
Name       Description                                       Default
=========  ================================================= ===========
*None*
=========  ================================================= ===========

Example Output
--------------
.. code-block:: python

    tree('yaml')

.. code-block:: yaml 

    author:
      genre: Fantasy/Comedy
      name: Terry Pratchett
      novels: [Small Gods, The Fifth Elephant, Guards! Guards!]
        
"""

from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

from .dictrender import DictRenderer

class YamlRenderer(DictRenderer):
    default_options = {
    }

    def render(self, base_node, options=None):
        """Renders the entire tree under base_node as a json string."""
        if options == None: options = {}
        return dump(self.render_final(self.render_node(base_node, options=options), options=options), Dumper=Dumper)
