API
===

.. module:: datatree

The API is mostly dynamic and so by nature difficult to document.  If you have
any suggestions for this please leave a note for me at 
`www.bigjason.com <http://www.bigjason.com/>`_.

Tree
----
You can call any method name on the :class:`Tree <datatree.Tree>` to create a 
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

    from datatree import Tree

    tree = Tree()
    with tree.author() as author:
        author.name('Terry Pratchett')
        author.genre('Fantasy/Comedy')
        author // "Only 2 books listed"
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)
            novels << Node("novel", "Guards! Guards!", year=1989)


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

ETreeRenderer
^^^^^^^^^^^^^
.. automodule:: datatree.render.etreerender