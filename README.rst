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
from the github_ repo.

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
    with tree.author() as author:
        author.name('Terry Pratchett')
        author.genre('Fantasy/Comedy')
        author // "Only 2 books listed"
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)
            novels << Node("novel", "Guards! Guards!", year=1989)

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
This work is licensed under the Creative Commons Attribution 3.0 Unported 
License. You can view a copy of this license `here <http://creativecommons.org/licenses/by/3.0/>`_.

Souce Code
----------
The source code can be found on github_.

Feedback
--------
I welcome any and all constructive feedback.  Feel free to contact me (Jason Webb) at 
`www.bigjason.com <http://www.bigjason.com/>`_ or on twitter 
`@bigjasonwebb <http://www.twitter.com/BigJasonWebb>`_.


.. _ruby builder: http://builder.rubyforge.org/
.. _github: https://github.com/bigjason/datatree