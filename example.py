from datatree.tree import Tree, Node

class NS(object):
    def __init__(self, node, namespace):
        if isinstance(namespace, tuple):
            self.prefix, self.namespace = namespace
        else:
            self.prefix = None
            self.namespace = namespace
        self.node = node
        
        node.__namespace__ = self.namespace
        node.__prefix__ = self.prefix
        
    def __enter__(self):
        return self.node

    def __exit__(self, exc_type, exc_value, traceback):
        return False

temp = """\
    <a:Envelope
        xmlns="http://default/"
        xmlns:a="http://urla"
        xmlns:b="http://urlb"
        xmlns:c="http://urlc"
        a:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <a:Header xmlns="" xmlns:b="http://alturlb">
        <b:type>HelloWorld</b:type>
        <c:to xmlns:c="http://alturlc">Mark Priest</c:to>
        <from fromType="name">John Smith</from>
      </a:Header>
      <a:Body>
        <text xmlns="http://newdefault">Hello</text>
        <b:mood>Happy</b:mood>
        <c:day>Friday</c:day>
        <month>January</month>
       </a:Body>
    </a:Envelope>
"""
if __name__ == '__main__':
    tree = Tree()
    tree.INSTRUCT('xml', version='1.0')
    tree.NS()
    with tree.author() as author:
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

