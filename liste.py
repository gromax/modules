'''
module: liste
synopsys: définition d'une liste au format liste chaînée
'''

class Noeud:
    '''
    noeud élémentaire de la liste
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

class Liste:
    '''
    Liste sous forme d'une liste chaînée
    '''

    def __init__(self):
        self.__head = None

    def length(self):
        '''
        Retourne le nombre d'éléments de la liste
        '''
        l = 0
        node = self.__head
        while node != None:
            l += 1
            node = node.getNext()
        return l

    def isEmpty(self):
        return self.__head == None

    def get(self, index):
        '''
        index: indice de l'item à lire
        result: valeur de l'élement de rang index dans la liste
        précondition : 0 <= index < longueur
        '''
        assert index >= 0, "index doit être >= 0"
        node = self.__head
        while node != None and index > 0:
            node = node.getNext()
            index -= 1
        assert node != None, "index >= longueur de la liste"
        return node.getValue()

    def __insertFirst(self, value):
        '''
        insère une valeur en première postion
        '''
        if self.__head != None:
            self.__head = self.__head.insertPrev(value)
            return
        node = Noeud(value)
        self.__head = node

    def insert(self, value, index):
        '''
        index: indice d'insertion
        value: valeur à insérer
        précondition: 0 <= index <= longueur
        '''
        assert index >= 0, "index doit être >= 0"
        if index == 0:
            self.__insertFirst(value)
            return
        node = self.__head
        while node != None and index > 1:
            node = node.getNext()
            index -= 1
        assert node != None, "index > longueur de la liste"
        node.insertNext(value)

    def indexOf(self, value):
        '''
        value: valeur recherchée
        result: rang de la première occurence trouvée, -1 si pas trouvé
        '''
        if self.isEmpty():
            return -1
        node = self.__head
        index = 0
        while node != None and node.value != value:
            index += 1
            node = node.getNext()
        if node == None:
            return -1
        return index

    def modify(self, index, value):
        '''
        index: indice de modification
        value: valeur à écrire
        précondition: 0 <= index < longueur
        '''
        assert i >= 0, "index doit être >= 0"
        node = self.__head
        while node != None and index > 0:
            node = node.getNext()
            index -= 1
        assert node != None, "index >= longueur de la liste"
        node.setValue(value)

    def pop(self):
        '''
        supprime la valeur en première position
        result: valeur supprimée
        précondition: liste non vide
        '''
        assert not self.isEmpty(), "Pop sur une liste est vide"
        delNode = self.__head
        self.__head = delNode.getNext()
        return delNode.getValue()

    def delete(self, index):
        '''
        index: rang de la valeur à supprimer
        result: valeur supprimée
        précondition: 0 <= index < longueur
        '''
        assert index >= 0
        if index == 0:
            return self.pop()
        node = self.__head
        while node != None and index > 2:
            node = node.getNext()
            index -= 1
        assert node != None, "index >= longueur de la liste"
        return node.deleteNext()

    # Fonctions supplémentaires

    def __str__(self):
        '''
        transtypage -> str
        '''
        if self.isEmpty():
            return "< >"
        return "<" + ":".join([str(it) for it in self]) + ">"

    def __iter__(self):
        return NodeIterator(self.__head)

    def __insertLast(self, value):
        '''
        value: valeur insèrée en queue
        '''
        if self.isEmpty():
            self.__insertFirst(value)
            return
        node = self.__head
        while node.getNext() != None:
            node = node.getNext()
        node.insertNext(value)

    @classmethod
    def make(cls, *items):
        '''
        crée une liste contenant les items passés en argument
        '''
        l = cls()
        for it in items:
            l.__insertLast(it)
        return l

    def __add__(L, N):
        '''
        Concaténation des listes L et N
        '''
        S = Liste()
        for it in L:
            S.__insertLast(it)
        for it in N:
            S.__insertLast(it)
        return S

if __name__ == '__main__':
    # tests
    L = Liste.make(4, 8, 9, 17, 25)
    print(L)
    print(L.length())
    L.insert(89, 3)
    print(L)
    L2 = Liste.make(14, 7, 3)
    M = L + L2
    print(M)

