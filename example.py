from datatree.node import Node

if __name__ == '__main__':
    author = Node('author')
    author.name('Terry Pratchett')
    author.genre('Fantasy/Comedy')
    author // "Only 2 books listed"
    with author.novels(count=2) as novels:
        novels.novel('Small Gods', year=1992)
        novels.novel('The Fifth Elephant', year=1999)

    print 'XML:'
    print author.render(pretty=True)
    print
    print 'JSON:'
    print author.render('json')
    print
    print 'YAML'
    print author.render('yaml')
    print
    print 'Dict:'
    print author.render('dict', pretty_string=True)
