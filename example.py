from datatree.node import Node

if __name__ == '__main__':
    author = Node('author')
    author.name('Terry Pratchett')
    author.genere('Fantasy/Comedy')
    with author.novels(count=2) as novels:
        novels.novel('Small Gods', year=1992)
        novels.novel('The Fifth Elephant', year=1999)

    print 'XML:'
    print author.render()
    print
    print 'JSON:'
    print author.render('json')
    print
    print 'Dict:'
    print author.render('dict')
