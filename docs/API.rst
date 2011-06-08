API
===

.. module:: datatree

The API is mostly dynamic and so by nature difficult to document.  If you have
any suggestions for this please leave a not for me at 
`bigjason.com <http://www.bigjason.com/>`_.

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

.. autoclass:: datatree.node.Node
   :inherited-members: