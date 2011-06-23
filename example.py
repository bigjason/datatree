from datatree.tree import Tree, Node

if __name__ == '__main__':
    
    with Tree().author() as author:
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
    print author('json', pretty=True)
    print
    print
    print 'YAML:'
    print author('yaml')
    print
    print
    print 'Dict:'
    print author('dict', pretty_string=True)
