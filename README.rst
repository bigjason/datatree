-------
Summary
-------
DataTree is a DSL for creating structured documents in python. Inspired by 
`ruby builder`_ but with the goal of reducing the amount of line noise associated 
with creating XML documents in python.  As an added bonus the tree can be output
to to any structured format (with XML, JSON and YAML supported in the library).

*Note:* More documentation is coming soon but for now a very basic rough draft can be
found at `datatree.readthedocs.org <http://datatree.readthedocs.org/>`_.

------------
Installation
------------
You can install via `PyPi <http://pypi.python.org/pypi/datatree/>`_ or direct 
from the github_ repository.

To install with pip::

    $ pip install datatree

To install with easy_install::

    $ easy_install datatree

-------
Example
-------
A small example::

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

    print tree(pretty=True) 

Which produces the XML::

    <author>
        <name>Terry Pratchett</name>
        <genre>Fantasy/Comedy</genre>
        <!-- Only 2 books listed -->
        <novels count="2">
            <novel year="1992">Small Gods</novel>
            <novel year="1999">The Fifth Elephant</novel>
            <novel year="1989">Guards! Guards!</novel>
        </novels>
    </author>

Or the JSON::

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

Or the YAML::

    author:
      genre: Fantasy/Comedy
      name: Terry Pratchett
      novels: [Small Gods, The Fifth Elephant, Guards! Guards!]


License
-------
This work is licensed under the `Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_.

Souce Code
----------
The source code can be found on github_.

Feedback
--------
I welcome any and all constructive feedback.  Feel free to contact me (Jason Webb) at 
`www.bigjason.com <http://www.bigjason.com/>`_ or (preferably) on twitter
`@bigjasonwebb <http://www.twitter.com/BigJasonWebb>`_.

Contributing
------------
Contributions are welcome.  Just fork on github_ and I will try to be as responsive
as possible.


.. _ruby builder: http://builder.rubyforge.org/
.. _github: https://github.com/bigjason/datatree