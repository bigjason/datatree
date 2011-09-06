from datatree import Tree

if __name__ == '__main__':
    tree = Tree()
    #tree.instruct('xml', version='1.0')
    with tree.node("author") as author:
        author.node('name', 'Terry Pratchett')
        author.node('genre', 'Fantasy/Comedy')
        author.comment("Only 2 books listed")
        with author.node('novels', count=2) as novels:
            novels.node('novel', 'Small Gods', year=1992)
            novels.node('novel', 'The Fifth Elephant', year=1999)
            novels.node("novel", "Guards! Guards!", year=1989)

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
