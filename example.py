from datatree.node import Tree, Node

if __name__ == '__main__':
    tree = Tree()
    with tree.author() as author:
        author.name('Terry Pratchett')
        author.genre('Fantasy/Comedy')
        author // "Only 2 books listed"
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)
            novels << Node("novel", "Guards! Guards!", year=1989)

    print 'XML:'
    print tree(pretty=True)
    print
    print
    print 'JSON:'
    print tree('json')
    print
    print
    print 'YAML:'
    print tree('yaml')
    print
    print
    print 'Dict:'
    print tree('dict', pretty_string=True)
