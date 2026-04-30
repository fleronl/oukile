class Noeud:
    """ Défini un noeud d'une arborescence"""

    def __init__(self, id, libelle, fils):
        self.id = id
        self.libelle = libelle
        self.fils = fils
    
    def __str__(self):
        return f"{self.libelle}({', '.join(str(f) for f in self.fils)})"
    
    def CreerArbre(self, liste):
        if not liste:
            return None
        id = liste[0]
        libelle = liste[1] if len(liste) > 1 else ""
        fils = []
        for i in range(2, len(liste)):
            fils.append(self.CreerArbre(liste[i]))
        return Noeud(id, libelle , fils)

if __name__ == "__main__":
    arbre = Noeud(1, "Batiment", [])
    arbre.fils.append(Noeud(2, "Salle 1", []))
    arbre.fils.append(Noeud(3, "Salle 2", []))
    print(arbre)

    # Exemple de création d'un arbre à partir d'une liste
    liste = [1, "Batiment", [2, "Salle 1"], [3, "Salle 2"]]
    arbre2 = Noeud(0, "", []).CreerArbre(liste)
    print(arbre2)


