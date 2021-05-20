'''
module: arbrebinairerecherche
'''

from noeudbinaire import NoeudBinaire
from pile import Pile
from file import File


class ArbreBinaire:
    _root = None

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
        output = []
        p = Pile()
        if self.isEmpty():
            p.push(self._root)
        while not p.isEmpty():
            node = p.pop()
            if node.hasRightChild():
                p.push(node.droit())
            if node.hasLeftChild():
                p.push(node.gauche())
            output.append(node)
        return output

    def parcours_largeur(self):
        '''
        Produit un <list> des éléments de l'arbre,
        parcourus en largeur
        '''
        output = []
        f = File()
        if self.isEmpty():
            f.push(self._root)
        while not f.isEmpty():
            node = f.pop()
            if node.hasRightChild():
                p.push(node.droit())
            if node.hasLeftChild():
                p.push(node.gauche())
            output.append(node)
        return output

    def __str__:
        t = self.parcours_profondeur_prefixe()
        outStrings = [" ↳"*node.profondeur() + str(node) for node in t]
        return "\n".join(outStrings)

class ArbreBinaireRecherche(ArbreBinaire):
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
        currentNodeKey = self.getKey(currentNode.value)
        while key != currentNodeKey:
            if key > currentNodeKey:
                # insertion à droite
                if not currentNode.hasRightChild():
                    currentNode.appendChildRight(newNode)
                    return self
                currentNode = currentNode.droit()
            else:
                if not currentNode.hasLeftChild():
                    currentNode.appendChildLeft(newNode)
                    return self
                currentNode = currentNode.gauche()
            currentNodeKey = self.getKey(currentNode.value)
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
        currentNodeKey = self.getKey(currentNode.value)
        while currentNode != None and currentNodeKey != key:
            if currentNodeKey < key:
                currentNode = currentNode.droit()
            else:
                currentNode = currentNode.gauche()
            currentNodeKey = self.getKey(currentNode.value)
        if currentNode == None:
            return None
        return currentNode.value





