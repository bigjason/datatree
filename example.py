from datatree.node import Tree, Name

if __name__ == '__main__':
    tree = Tree()
    tree.INSTRUCT('xml')
    tree.DECLARE('ELEMENT', Name.Value, 'A value here.')
    with tree.author() as author: 
        author.name('Terry Pratchett')
        author.genre('Fantasy/Comedy')
        author // "Only 2 books listed"
        with author.novels(count=2) as novels:
            novels.novel('Small Gods', year=1992)
            novels.novel('The Fifth Elephant', year=1999)

    print 'XML:'
    print tree.render(pretty=True)
    print
    print 'JSON:'
    print tree.render('json')
    print
    print 'YAML'
    print tree.render('yaml')
    print
    print 'Dict:'
    print tree.render('dict', pretty_string=True)
