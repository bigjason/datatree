from datatree.node import Tree

if __name__ == '__main__':
    tree = Tree()
    with tree.author() as author:
        author.name('Terry Pratchett')
        author.genre('Fantasy/Comedy')
        author // "Only 2 books listed"
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)

    print 'XML:'
    print tree(pretty=True)
    print
    print 'JSON:'
    print tree('json')
    print
    print 'YAML'
    print tree('yaml')
    print
    print 'Dict:'
    print tree('dict', pretty_string=True)

    tree = Tree()
    with tree.root() as root:
        root.name("Bob Smith", full=True)
    print tree('xml', pretty=True)
    
