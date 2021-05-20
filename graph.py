'''
module graph: définition d'une classe Graph
'''

# on inclut une version limitée de File
# pour les besoins des parcours en largeur

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

class Graph:
    def __init__(self, oriented = False):
        '''_vertex : dictionnaire donc chaque paire est :
             clé : étiquette d'un sommet
             valeur: tableau des sommets pouvant être atteints
        '''
        self._vertex = {}
        # rappel : self._vertex.keys() -> tableau des clés
        self._oriented = oriented

    def ordre(self):
        '''
        renvoie l'ordre du graphe
        '''
        return len(self._vertex)

    def add_vertex(self, label):
        '''
        ajoute un sommet
        label : étiquette du sommet. label de n'importe quel type.
        précondition : il n'y a pas déjà ce label dans le graphe
        '''
        assert not self.has_vertex(label)
        self._vertex[label] = []

    def add_edge(self, label1, label2):
        '''
        ajoute une arête entre les sommets étiquetés par label1 et label2
        préconditions :
          les sommets existent dans le graphe
          il n'y a pas déjà d'arête entre ces sommets
          label1 != label2
        '''
        if self._oriented:
            # cas graphe orienté
            assert not self.is_successor(label1, label2), "L'arête existe déjà"
            self._vertex[label1].append(label2)
        else:
            # non orienté
            assert label1 != label2, "Les deux sommets doivent être distincts"
            assert not self.are_neighbours(label1, label2), "L'arête existe"
            self._vertex[label1].append(label2)
            self._vertex[label2].append(label1)

    def remove_edge(self, label1, label2):
        '''
        supprime une arête entre les sommets étiquetés par label1 et label2
        préconditions :
          les sommets existent dans le graphe
          il y a une arête entre ces sommets
        '''
        if not self._oriented:
            assert self.are_neighbours(label1, label2)
            self._vertex[label1].remove(label2)
            self._vertex[label2].remove(label1)
        else:
            assert self.is_successor(label1, label2)
            self._vertex[label1].remove(label2)

    def are_neighbours(self, label1, label2):
        '''
        renvoie True si les labels existent dans le graphe
        et qu'ils sont voisins. False sinon.
        '''
        assert self.has_vertex(label1)
        assert self.has_vertex(label2)
        return label1 in self._vertex[label2] and label2 in self._vertex[label1]

    def has_vertex(self, label):
        '''
        renvoie True s'il y a un sommet étiqueté label dans le graphe
        '''
        return label in self._vertex
        # ou encore :
        if label in self._vertex:
            return True
        return False

    def degre(self, label, sortant = True):
        '''
        renvoie le degré du sommet étiqueté par label dans le graphe
        sortant : True si on demande le degré sortant
          sans effet pour un graphe non orienté
        précondition : le sommet existe
        '''
        if not self._oriented or sortant:
            return len(self.successors(label))
        # cas orienté et entrant
        return len(self.antecedents(label))

    def is_successor(self, label1, label2):
        '''
        renvoie True si label1 -> label2
        précondition: label1 dans le graph
        '''
        return label2 in self.successors(label1)


    def successors(self, label):
        '''
        renvoie le tableau des successeurs de label
        précondtion: label est dans le graphe
        '''
        assert self.has_vertex(label), "Le sommet {} n'est pas dans le graphe".format(label)
        return self._vertex[label].copy()

    def antecedents(self, label):
        '''
        renvoie le tableau des antecedents de label
        précondtion: label est dans le graphe
        '''
        assert self.has_vertex(label), "Le sommet {} n'est pas dans le graphe".format(label)
        return [label2 for label2 in self._vertex if self.is_successor(label2, label)]

    def adjacence(self):
        labels = list(self._vertex.keys())
        matrice = []
        for labelSource in labels:
            line = []
            for labelDest in labels:
                if self.is_successor(labelSource, labelDest):
                    line.append(1)
                else:
                    line.append(0)
            matrice.append(line)
        return labels, matrice


    def __str__(self):
        output = []
        for label in self._vertex:
            voisins = [str(it) for it in self.successors(label)]
            line = "{} -> {}".format(label, ', '.join(voisins) )
            output.append(line)
        return "\n".join(output)

    def has_cycle(self):
        '''
        result: True si le graphe contient un cycle
        précondition : graphe non-orienté
        '''
        assert not self._oriented, "La méthode has_cycle ne fonctionne que pour le cas non-orienté"
        marques = {}
        for v in self._vertex:
            marques[v] = None
        f = File()

        notVisited = [vertex for vertex in self._vertex]
        while notVisited != []:
            firstVertex = notVisited.pop()
            marques[firstVertex] = 0
            f.push(firstVertex)
            while not f.isEmpty():
                s = f.pop()
                for v in self.successors(s):
                    if marques[v] == None:
                        marques[v] = marques[s] + 1
                        f.push(v)
                        notVisited.remove(v)
                    elif marques[v] >= marques[s]:
                        print(v)
                        print(s)
                        return True
        return False

    def coloration(self):
        '''
        result: dict dont les sommets sont les clés, les valeurs un numéro représentant une couleur
        '''
        assert not self._oriented, "La coloration recquiert un graphe non orienté."
        couleurs = {} # couleurs attribuées
        #sommets par ordre décroissant de degré
        vertexList = list(self._vertex.keys())
        N = len(vertexList)
        vertexList.sort(key=self.degre, reverse=True)
        col = 0
        for index in range(N):
            sommet = vertexList[index]
            if sommet in couleurs:
                # déjà coloré, on passe au suivant
                continue
            couleurs[sommet] = col
            # recherche des sommets suivants
            for sommet in vertexList[index+1:]:
                if sommet not in couleurs and not self._hasAdjacentCol(sommet, col, couleurs):
                    couleurs[sommet] = col
            col += 1
        return couleurs

    def _hasAdjacentCol(self, sommet, col, couleurs):
        '''
        méthode accessoire : vérifie si le sommet a déjà un
        voisin de la couleur col
        '''
        for voisin in self.successors(sommet):
            if couleurs.get(voisin) == col:
                return True
        return False



if __name__ == "__main__":
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_vertex("D")
    g.add_edge("A","B")
    g.add_edge("A","C")
    g.add_edge("B","C")
    g.add_edge("C","D")

    print(g.coloration())
