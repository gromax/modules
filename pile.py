'''
module: pile
synopsys: définition d'une pile au format liste chaînée
'''

class Noeud:
    '''
    noeud élémentaire de la pile
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

    def cutNext(self):
        if self.__next != None:
            self.__next.__orphan = True
        self.__next = None

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

class NodeIterator:
    def __init__(self, node):
        self.__node = node

    def __next__(self):
        if self.__node == None:
            raise StopIteration
        value = self.__node.getValue()
        self.__node = self.__node.getNext()
        return value

class Pile:
    '''
    Pile sous forme d'une liste chaînée
    '''

    def __init__(self, maxSize = 0):
        self.__head = None
        self.__count = 0
        self.__maxSize = maxSize

    def length(self):
        """
        :returns: le nombre d'éléments de la pile
        """
        return self.__count

    def isEmpty(self):
        return self.__head == None

    def push(self, value):
        '''
        insère une valeur en première postion
        précondition : pas déjà plein
        '''
        assert self.__maxSize == 0 or self.__maxSize > self.__count, "Pile pleine"
        self.__count += 1
        if self.__head != None:
            self.__head = self.__head.insertPrev(value)
            return
        node = Noeud(value)
        self.__head = node

    def pop(self):
        '''
        supprime la valeur en première position
        result: valeur supprimée
        précondition: pile non vide
        '''
        assert not self.isEmpty(), "Pop sur une pile est vide"
        self.__count -= 1
        delNode = self.__head
        self.__head = delNode.getNext()
        delNode.cutNext()
        return delNode.getValue()

    # Fonctions supplémentaires

    def __str__(self):
        '''
        transtypage -> str
        '''
        if self.isEmpty():
            return "< >"
        return ">>[" + ":".join([str(it) for it in self]) + "]"

    def __iter__(self):
        return NodeIterator(self.__head)

    @classmethod
    def make(cls, *items):
        '''
        crée une pile contenant les items passés en argument
        '''
        p = cls()
        for it in items[::-1]:
            p.push(it)
        return p

if __name__ == '__main__':
    # tests
    P = Pile.make(4, 8, 9, 17, 25)
    print(P)
    print(P.length())
    P.push(89)
    print(P)
    print(P.pop())
    print(P.pop())
    print(P)


