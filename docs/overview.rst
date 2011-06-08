Basic Usage
===========

Building Data Trees
-----------------------------
Working with datatree begins with the :class:`Tree <datatree.Tree>` class:

.. code-block:: python

    tree = Tree()

To add a new node to the ``tree`` you simply call a function with the name of the
new node that you wish to add.  So to add a ``root`` node to the tree you could:

.. code-block:: python

    tree.root()

All nodes are also context managers.  This allows for very logical building of the
tree like so::

    with tree.root() as root:
        root.name("Bob Smith")

There are some various options when adding nodes, although most of them are only
relevent if you are creating XML.  When adding a node, any ``**kwargs`` argument
passed in is converted to an attribute::

    with tree.root() as root:
        root.name("Bob Smith", gender='Male')

Emitting Formatted Data
-----------------------
Renderers are used to output your datatree into a dataformat.  These are simple
classes that translate the :class:`Tree <datatree.Tree>` into a specific format. By
default XML is used.  However an alias can be used for a different format. Additionaly
all of the ``**kwargs`` are used to pass specific options to the renderer. To output
pretty XML::

    tree = Tree()
    with tree.root() as root:
        root.name("Bob Smith", full=True)
    print tree('xml', pretty=True)
    
Outputs:

.. code-block:: xml 

    <root>
        <name full="True">Bob Smith</name>
    </root>

The aliases for the formats are as follows:

+----------------------------+--------------------+
| Renderer                   | Alias(s)           |
+============================+====================+
| XML                        | xml, [blank]       |
+----------------------------+--------------------+
| JSON                       | json, jsn          |
+----------------------------+--------------------+
| YAML                       | yaml, yml          |
+----------------------------+--------------------+
| Python dict                | dict, dictionary   |
+----------------------------+--------------------+
 