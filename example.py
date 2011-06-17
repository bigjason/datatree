from datatree.node import Tree, Node

if __name__ == '__main__':
    author = Tree().author()
    author.name('Terry Pratchett')
    author.genre('Fantasy/Comedy')
    author // "Only 2 books listed"
    with author.novels(count=2) as novels:
        novels.novel('Small Gods', year=1992)
        novels.novel('The Fifth Elephant', year=1999)
        novels << Node("novel", "Guards! Guards!", year=1989)

    print 'XML:'
    print author(pretty=True)
    print
    print
    print 'JSON:'
    print author('json')
    print
    print
    print 'YAML:'
    print author('yaml')
    print
    print
    print 'Dict:'
    print author('dict', pretty_string=True)
