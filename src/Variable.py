
class Variable(object):

    def __init__(self, value = None, type = None, alias = None, name = None):
        self.name = name
        self.value = value
        self.type = type
        self.alias = alias
        self.arrayType = None
        
    def __str__(self):
        return str(self.value) + ' - ' + str(self.type)


