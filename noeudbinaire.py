''''
module : noeudbinaire
  Définition d'un noeud binaire pour arbre binaire
'''

class NoeudBinaire:

    def __init__(self, value):
        '''Initialisation du noeud
        value: valeur stockée dans le noeud
        '''
        self._parent        = None
        self._enfantGauche  = None
        self._enfantDroit   = None
        self.value         = value

    def gauche(self):
      '''
      renvoie l'enfant gauche
      '''
      return self._enfantGauche

    def hasLeftChild(self):
      '''
      renvoie True s'il y a un enfant à gauche
      '''
      return self._enfantGauche != None

    def droit(self):
      '''
      renvoie l'enfant droit
      '''
      return self._enfantDroit

    def hasRightChild(self):
      '''
      renvoie True s'il y a un enfant à droite
      '''
      return self._enfantDroit != None

    def parent(self):
      '''
      renvoie le parent
      '''
      return self._parent

    def isRoot(self):
      '''
      renvoie True si le nœud n'a pas de parent
      '''
      return self._parent == None

    def hauteur(self):
        '''
        result: la hauteur du sous-arbre issu du noeur
        '''
        if self.enfantGauche == None and self._enfantDroit == None:
            return 0
        if self._enfantGauche == None:
            return self._enfantDroit.hauteur() + 1
        if self._enfantDroit == None:
            return self._enfantGauche.hauteur() + 1
        return 1 + max(self._enfantDroit.hauteur(), self._enfantGauche.hauteur())

    def profondeur(self):
        '''
        result: profondeur du noeud
        '''
        if self._parent == None:
            return 0
        return self._parent.profondeur() + 1

        # autre méthode
        '''
        p = 0
        node = self
        while node._parent != None:
            p = p + 1
            node = node._parent
        return p
        '''

    def getRoot(self):
        '''
        result: noeud racine de l'arbre dont ce noeud est membre
        '''
        if self._parent == None:
            return self
        return self._parent.getRoot()

    def clone(self):
        pass

    def __str__(self):
        return str(self.value)

    def appendChildLeft(self, child):
        '''
        child : enfant attaché à gauche de ce noeud.
        préconditions : child n'a pas de parent et n'est pas racine de ce noeud
          et ce noeud n'a pas déjà un enfant à gauche.
        '''
        assert self._enfantGauche == None, "le _parent a déjà un enfant à gauche"
        assert child._parent == None, "l'enfant a déjà un _parent"
        assert child != self.getRoot(), "l'enfant ne doit pas être la racine de l'arbre"
        self._enfantGauche = child
        child._parent = self

    def appendChildRight(self, child):
        '''
        child : enfant attaché à droite de ce noeud.
        préconditions : child n'a pas de parent et n'est pas racine de ce noeud
          et ce noeud n'a pas déjà un enfant à droite.
        '''

        assert self._enfantDroit == None, "le _parent a déjà un enfant à droite"
        assert child._parent == None, "l'enfant a déjà un _parent"
        assert child != self.getRoot(), "l'enfant ne doit pas être la racine de l'arbre"

        self._enfantDroit = child
        child._parent = self

if __name__ == "__main__":
    n = NoeudBinaire(45)
    m = NoeudBinaire(18)
    n.appendChildLeft(m)
