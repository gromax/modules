'''
module: arbre
'''

# on inclut une version limitée de Pile et File
# pour les besoins des parcours en largeur et profondeur

class Maillon:
    # maillon pour File et Pile
    def __init__(self, value):
        self.value = value
        self.next = None

class File:
    # version réduite de la classe File
    def __init__(self):
        self.__root = None
        self.__last = None
    def isEmpty(self):
        return self.__root == None
    def push(self, value):
        # insertion en bout de file
        if self.__root == None:
            self.__root = Maillon(value)
            self.__last = self.__root
            return
        newM = Maillon(value)
        self.__last.next = newM
        self.__last = newM
    def pop(self):
        assert not self.isEmpty(), "La file est vide"
        headingMaillon = self.__root
        self.__root = headingMaillon.next
        if self.__root == None:
            self.__last = None
        headingMaillon.next = None
        return headingMaillon.value

class Pile:
    # version réduite de la classe Pile
    def __init__(self):
        self.__root = None
    def isEmpty(self):
        return self.__root == None
    def push(self, value):
        # insertion en tête de file
        newM = Maillon(value)
        newM.next = self.__root
        self.__root = newM
    def pop(self):
        assert not self.isEmpty(), "La pile est vide"
        headingMaillon = self.__root
        self.__root = headingMaillon.next
        headingMaillon.next = None
        return headingMaillon.value


class Noeud:
    def __init__(self, value):
        '''Initialisation du noeud
        value: valeur stockée dans le noeud
        '''
        self._parent = None
        self._childs = []
        self._value   = value

    def hauteur(self):
        '''
        result: la hauteur du sous-arbre issu du noeud
        '''
        subHauteurs = [child.hauteur() for child in self._childs if child != None]
        if len(subHauteurs) == 0:
            return 0
        return 1 + max(subHauteurs)

    def profondeur(self):
        '''
        result: profondeur du noeud
        '''
        if self._parent == None:
            return 0
        return self._parent.profondeur() + 1

    def getRoot(self):
        '''
        result: noeud racine de l'arbre dont ce noeud est membre
        '''
        if self._parent == None:
            return self
        return self._parent.getRoot()

    def __str__(self):
        return str(self._value)

    def appendChild(self, child):
        '''
        child : enfant à attacher.
        préconditions : child n'a pas de parent et n'est pas racine de ce noeud
          et ce noeud n'a pas déjà un enfant à gauche.
        '''
        assert type(child) == Noeud, "Noeud.AppendChild demande un objet de type Noeud"
        assert child._parent == None, "l'enfant a déjà un _parent"
        assert child != self.getRoot(), "l'enfant ne doit pas être la racine de l'arbre"
        self._childs.append(child)
        child._parent = self

    def appendValue(self, value):
        '''
        value : valeur à ajouter en tant qu'enfant
        return: nœud créé
        '''
        node = Noeud(value)
        self.appendChild(node)
        return node

    def getChilds(self):
        '''renvoie un tuple avec les enfants
        '''
        return tuple(self._childs)

    def parcours_profondeur_prefixe(self):
        '''
        Produit un <list> des éléments du sous arbre démarrant avec ce noeud,
        parcouru en profondeur, dans un ordre prefixe
        '''
        output = []
        p = Pile()
        p.push(self)
        while not p.isEmpty():
            node = p.pop()
            childs = node.getChilds()
            for c in childs[::-1]:
                p.push(c)
            output.append(node)
        return output

    def parcours_largeur(self, filter = None):
        '''
        Produit un <list> des éléments du sous arbre démarrant avec ce noeud,
        parcourus en largeur
        filter: fonction permettat de ne conserver que les nœuds validant une condition
        '''
        output = []
        f = File()
        f.push(self)
        while not f.isEmpty():
            node = f.pop()
            childs = node.getChilds()
            for c in childs:
                f.push(c)
            if filter == None or filter(node):
                output.append(node)
        return output

    def isLeaf(self):
        '''
        Prédicat : renvoie True si le noeud est une feuille (n'a pas d'enfants)
        '''
        return len(self._childs) == 0

    def getLeafs(self):
        '''renvoie les feuilles du sous arbre démarrant avec ce noeud
        '''
        return self.parcours_largeur(lambda node: node.isLeaf())

    def removeChild(self, child):
        '''
        Détache child.
        Renvoie True si c'est un succès.
        '''
        if not child in self._childs:
            return False
        child.parent = None
        index = self._childs.index(child)
        self._childs.pop(index)
        return True

    def getBranchValues(self):
        '''
        Renvoie le tableau des valeurs de la branche de ce nœud
        partant de ce nœud et remontant vers la racine
        '''
        node = self
        values = []
        while node != None:
            values.append(node.getValue())
            node = node._parent
        return values

    def getValue(self):
        return self._value

    def getParent(self):
        '''
        renvoie le parent
        '''
        return self._parent

class NoeudBinaire(Noeud):

    def __init__(self, value):
        '''Initialisation du noeud
        value: valeur stockée dans le noeud
        '''
        self._parent        = None
        self._childs       = tuple()
        self._leftChild    = None
        self._rightChild   = None
        self._value         = value

    def appendChild(self, child):
        '''
        child : enfant à attacher.
        Inserre à gauche ou à droite suivant la place dispo
        '''
        assert len(self._childs) < 2, "Ce noeud a déjà deux enfants"
        if self._leftChild == None:
            self.appendChildLeft(child)
        self.appendChildRight(child)

    def appendChildLeft(self, child):
        '''
        child : enfant attaché à gauche de ce noeud.
        préconditions : child n'a pas de parent et n'est pas racine de ce noeud
          et ce noeud n'a pas déjà un enfant à gauche.
        '''
        assert self._leftChild == None, "le _parent a déjà un enfant à gauche"
        assert child._parent == None, "l'enfant a déjà un _parent"
        assert child != self.getRoot(), "l'enfant ne doit pas être la racine de l'arbre"
        self._leftChild = child
        self._childs = self.getChilds()
        child._parent = self

    def appendChildRight(self, child):
        '''
        child : enfant attaché à droite de ce noeud.
        préconditions : child n'a pas de parent et n'est pas racine de ce noeud
          et ce noeud n'a pas déjà un enfant à droite.
        '''

        assert self._childs[1] == None, "le _parent a déjà un enfant à droite"
        assert child._parent == None, "l'enfant a déjà un _parent"
        assert child != self.getRoot(), "l'enfant ne doit pas être la racine de l'arbre"
        self._rightChild = child
        self._childs = self.getChilds()
        child._parent = self

    def hasLeftChild(self):
        '''
        prédicat : renvoie True s'il y a un enfant gauche
        '''
        return self._leftChild != None


    def hasRightChild(self):
        '''
        prédicat : renvoie True s'il y a un enfant droit
        '''
        return self._rightChild != None

    def getLeftChild(self):
        '''
        Accesseur : renvoie l'enfant gauche
        '''
        return self._leftChild

    def getRightChild(self):
        '''
        Accesseur : renvoie l'enfant droit
        '''
        return self._rightChild

    def removeChild(self, child):
        '''
        Détache child.
        Renvoie True si c'est un succès.
        '''
        if not child in self._childs:
            return False
        child.parent = None
        if self._leftChild == child:
            self._leftChild = None
        else:
            self._rightChild = None
        self._childs = self.getChilds()
        return True

    def getChilds(self):
        '''renvoie un tuple avec les enfants
        '''
        if self._leftChild == None:
            if self._rightChild == None:
                return tuple()
            return (self._rightChild,)
        if self._rightChild == None:
                return (self._leftChild,)
        return (self._leftChild, self._rightChild)


class Arbre:
    _root = None

    def __init__(self, root):
        self._root = root

    def isEmpty(self):
        '''
        renvoie True si l'arbre est vide
        '''
        return self._root == None

    def parcours_profondeur_prefixe(self):
        '''
        Produit un <list> des éléments de l'arbre,
        parcourus en profondeur, dans un ordre prefixe
        '''
        if self.isEmpty():
            return []
        return self._root.parcours_profondeur_prefixe()

    def parcours_largeur(self):
        '''
        Produit un <list> des éléments de l'arbre,
        parcourus en largeur
        '''
        if self.isEmpty():
            return []
        return self._root.parcours_largeur()

    def __str__(self):
        t = self.parcours_profondeur_prefixe()
        def formatage(node):
            p = node.profondeur()
            if p > 0:
                marge = "  "*(p-1) + " ↳ "
            else:
                marge = " "
            return marge + str(node)
        outStrings = [formatage(node) for node in t]
        return "\n".join(outStrings)

    def getLeafs(self):
        '''
        renvoie les feuilles de l'arbre
        '''
        if self.isEmpty():
            return []
        return self._root.getLeafs()

class ArbreBinaireRecherche(Arbre):
    def __init__(self, getKey):
        '''initialisation de l'arbre
        getKey: fonction qui extrait la clé de trie d'une valeur de noeud.
          exemple, si on a des valeurs type (nom, numéro), getKey pourrait extraire le nom
        '''
        self.getKey = getKey

    def insert(self, value):
        '''insert un nouveau nœud contenant value
        value : valeur du nœud à créer
        renvoie l'arbre lui même
        '''
        newNode = NoeudBinaire(value)
        if self.isEmpty():
            self._root = newNode
            return self
        key = self.getKey(value)
        currentNode = self._root
        currentNodeKey = self.getKey(currentNode.getValue())
        while key != currentNodeKey:
            if key > currentNodeKey:
                # insertion à droite
                if not currentNode.hasRightChild():
                    currentNode.appendChildRight(newNode)
                    return self
                currentNode = currentNode.getRightChild()
            else:
                if not currentNode.hasLeftChild():
                    currentNode.appendChildLeft(newNode)
                    return self
                currentNode = currentNode.getLeftChild()
            currentNodeKey = self.getKey(currentNode.getValue())
        # on arrive ici si la clé existe déjà
        return self

    def get(self, key):
        '''
        renvoie la valeur du nœud dont la clé est key
        si elle existe. Sinon renvoie None
        '''
        if self.isEmpty():
            return None
        currentNode = self._root
        currentNodeKey = self.getKey(currentNode.getValue())
        while currentNode != None and currentNodeKey != key:
            if currentNodeKey < key:
                currentNode = currentNode.getRightChild()
            else:
                currentNode = currentNode.getLeftChild()
            currentNodeKey = self.getKey(currentNode.getValue())
        if currentNode == None:
            return None
        return currentNode.getValue()




if __name__ == '__main__':
    r1 = Noeud("A")
    r2 = Noeud("B")
    r3 = Noeud("C")
    r4 = Noeud("D")
    r5 = Noeud("E")
    r6 = Noeud("F")
    r7 = Noeud("G")

    r1.appendChild(r2)
    r1.appendChild(r3)
    r2.appendChild(r4)
    r2.appendChild(r5)
    r5.appendChild(r6)
    r3.appendChild(r7)
    print([str(item) for item in r1.parcours_largeur()])
    print([str(item) for item in r1.getLeafs()])

    a = Arbre(r1)
    print(a)
