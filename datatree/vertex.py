from StringIO import StringIO

class Vertex(object):

    def __init__(self, name, value=None, parent=None, **kwargs):
        self.__name__ = name
        self.__value__ = value
        self.__parent__ = parent
        self.__children = []
        self.__attributes__ = kwargs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def add(self, name, value=None, parent=None, **kwargs):
        result = Vertex(
            name=name,
            value=value,
            parent=self, 
            **kwargs
        )
        self.__children.append(result)
        return result
        
    """
    def __getattribute__(self, name):
        try:
            if name.startswith("__") and name.endswith("__"):
                val = object.__getattribute__(self, name)
                return val
            else:
                raise ValueError()
        except:
            temp = Vertex(name=name, parent=self)
            self.children.append(temp)
            return temp
    
    def __setattr__(self, name, value):
        if name.startswith("__") and name.endswith("__"):
            self.__dict__[name] = value
    """

    def __str__(self):
        return "Node: {}, Value: {}".format(self.__name__, self.__value__)
        
    def to_string(self, level=0):
        new_level = level + 1
        result = StringIO()
        result.write(str(self))

        for child in self.__children:
            result.write("\n")            
            result.write("  " * new_level)
            result.write(child.to_string(new_level))
            
        return result.getvalue()

class Builder(object):
    pass

a = Vertex("root")
with a as node:
    node.add("name", "Jason")
    with node.add("Fame", "Nothing Much Here") as Fame:
        Fame.add("Doing", "It")
    node.add("Face", "Pale")

    #a.phone = "Webb"

print a.to_string()
