'''
module: file
synopsys: définition d'une file au format liste chaînée
'''

class Noeud:
    '''
    noeud élémentaire de la file
    '''
    def __init__(self, value):
      '''
      value: valeur du noeud à créer
      '''
      self.__value = value
      self.__next = None
      self.__orphan = True # n'a pas de prédecesseur

    def __str__(self):
        return str(self.__value)

    def getNext(self):
        return self.__next

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value = value

    def insertPrev(self, value):
        '''
        value: valeur inserrée à gauche
        result: le noeud créé
        précondition : self est orphelin
        '''
        assert self.__orphan, "Impossible d'insérer à gauche, le nœud n'est pas orphelin."
        node = Noeud(value)
        node.__next = self
        self.__orphan = False
        return node

    def insertNext(self, value):
        '''
        value: valeur inserrée à droite
        '''
        node = Noeud(value)
        node.__next = self.__next
        self.__next = node
        node.__orphan = False

    def deleteNext(self):
        '''supprime l'élément suivant
        retourne la valeur de l'élément supprimé
        '''
        assert self.__next != None, "Pas d'élément suivant à supprimer"
        delNode = self.__next
        self.__next = delNode.__next
        delNode.__next = None
        delNode.__orphan = True
        return delNode.getValue()

class NodeIterator:
    def __init__(self, node):
        self.__node = node

    def __next__(self):
        if self.__node == None:
            raise StopIteration
        value = self.__node.getValue()
        self.__node = self.__node.getNext()
        return value

class File:
    '''
    File sous forme d'une liste chaînée
    '''

    def __init__(self, maxSize = 0):
        self.__head = None
        self.__count = 0
        self.__maxSize = maxSize

    def length(self):
        '''
        Retourne le nombre d'éléments de la file
        '''
        return self.__count

    def isEmpty(self):
        return self.__head == None


    def push(self, value):
        '''
        insère une valeur en première postion
        '''
        assert self.__maxSize == 0 or self.__maxSize > self.__count, "File pleine"
        self.__count += 1
        if self.__head != None:
            self.__head = self.__head.insertPrev(value)
            return
        node = Noeud(value)
        self.__head = node

    def pop(self):
        '''
        supprime la valeur en dernière position
        result: valeur supprimée
        précondition: file non vide
        '''
        assert not self.isEmpty(), "Pop sur une file est vide"
        self.__count -= 1
        node = self.__head
        nextNode = node.getNext()
        if nextNode == None:
            value = self.__head.getValue()
            self.__head = None
            return value
        while nextNode.getNext() != None:
            node = nextNode
            nextNode = nextNode.getNext()
        return node.deleteNext()

    # Fonctions supplémentaires

    def __str__(self):
        '''
        transtypage -> str
        '''
        if self.isEmpty():
            return "< >"
        return ">[" + ":".join([str(it) for it in self]) + "]>"

    def __iter__(self):
        return NodeIterator(self.__head)


    @classmethod
    def make(cls, *items):
        '''
        crée une file contenant les items passés en argument
        '''
        f = cls()
        for it in items[::-1]:
            f.push(it)
        return f

if __name__ == '__main__':
    # tests
    F = File.make(4, 8, 9, 17, 25)
    print(F)
    print(F.length())
    F.push(89)
    print(F)
    print(F.pop())
    print(F.pop())
    print(F)

