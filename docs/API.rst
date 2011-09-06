API
===

.. module:: datatree


Tree
----
You can call (*almost*) any method name on the :class:`Tree <datatree.Tree>` to create a 
new Node.

.. autoclass:: datatree.Tree
   :inherited-members:
   
Node
----
Node is not instantiated directly, but is created for every node added to the 
:class:`Tree <datatree.Tree>`.

.. autoclass:: datatree.tree.Node
   :inherited-members:
   
Renderers
---------
The renderers are responsible for converting the datatree into a usable 
format. Usually this format is a string, but sometimes other formats are 
used.

The examples in this section use this datatree::

    from datatree import Tree, Node

    tree = Tree()
    with tree.node("author") as author:
        author.node('name', 'Terry Pratchett')
        author.node('genre', 'Fantasy/Comedy')
        author.comment("Only 2 books listed")
        with author.node('novels', count=2) as novels:
            novels.node('novel', 'Small Gods', year=1992)
            novels.node('novel', 'The Fifth Elephant', year=1999)
            novels.node("novel", "Guards! Guards!", year=1989)


XmlRenderer
^^^^^^^^^^^
.. automodule:: datatree.render.xmlrenderer 

JsonRenderer
^^^^^^^^^^^^
.. automodule:: datatree.render.jsonrender 

YamlRenderer
^^^^^^^^^^^^
.. automodule:: datatree.render.yamlrender 

DictRenderer
^^^^^^^^^^^^
.. automodule:: datatree.render.dictrender 

Implementing a Renderer
^^^^^^^^^^^^^^^^^^^^^^^
You can implement your own renderer.  Just look at the source for one of the 
existing renderers and implement the same methods, and then register your plugin
with the :meth:`~datatree.Tree.register_renderer` method.