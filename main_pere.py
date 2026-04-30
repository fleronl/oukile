"""
Dans cette implémentation, nous avons défini une classe `Noeud` qui représente 
un noeud dans une arborescence.

Chaque noeud a :
- un identifiant (`id`),
- un libellé (`libelle`)
- un père (`pere`) qui est un autre noeud ou `None` s'il n'a pas de père comme la racine de l'arbre.

La méthode `CreerArbre` permet de construire une arborescence à partir d'une liste imbriquée, 
où le premier élément est l'identifiant, le deuxième est le libellé, 
et l'élément précend est le père'.
"""

class ArticleNode:
    """
    Représente un nœud dans l'arbre des articles sans redondance.
    """
    def __init__(self, id, code_article, libelle, pere=None):
        self.id = id
        self.code_article = code_article
        self.libelle = libelle
        self.pere = pere  # ID du parent (unique lien de parenté)

    def __repr__(self):
        return f"Node({self.code_article}: {self.libelle})"


class ArticleTree:
    """
    Gère la hiérarchie des articles en utilisant uniquement l'attribut 'pere'.
    """
    def __init__(self):
        self.nodes = {}  # Stockage à plat des nœuds par ID

    def ajouter_depuis_liste(self, liste_articles):
        """
        Remplit le dictionnaire de nœuds à partir d'une liste brute.
        """
        for item in liste_articles:
            node = ArticleNode(
                id = item['id'],
                code_article = item['code_article'],
                libelle = item['libelle'],
                pere = item['pere']
            )
            self.nodes[node.id] = node

    def trouver_enfants(self, parent_id):
        """
        Recherche dynamiquement tous les nœuds ayant un parent spécifique.
        """
        return [node for node in self.nodes.values() if node.pere == parent_id]

    def afficher_arbre(self, parent_id=None, niveau=0):
        """
        Affiche l'arbre de manière récursive en filtrant par l'ID du père.
        """
        # On récupère les nœuds qui ont parent_id comme père
        enfants = self.trouver_enfants(parent_id)
        
        for n in enfants:
            indentation = "  " * niveau
            prefixe = "└── " if niveau > 0 else "• "
            print(f"{indentation}{prefixe}[{n.code_article}] {n.libelle}")
            
            # Appel récursif pour chercher les enfants de ce nœud
            self.afficher_arbre(n.id, niveau + 1)


# --- EXEMPLE D'UTILISATION : GESTION D'UN BÂTIMENT ---

if __name__ == "__main__":
    # Liste simulant la hiérarchie : Bâtiment > Salle > Casier > Livre
    donnees_articles = [
        # Niveau 0 : Le Bâtiment
        {"id": 1, "code_article": "BAT-A", "libelle": "Bâtiment Principal", "pere": None},
        
        # Niveau 1 : Les Salles (parent = Bâtiment)
        {"id": 10, "code_article": "S01", "libelle": "Salle de Stockage Nord", "pere": 1},
        {"id": 11, "code_article": "S02", "libelle": "Salle de Lecture", "pere": 1},
        
        # Niveau 2 : Les Casiers (parent = Salles)
        {"id": 100, "code_article": "C-A1", "libelle": "Casier Métallique A1", "pere": 10},
        {"id": 101, "code_article": "C-A2", "libelle": "Casier Métallique A2", "pere": 10},
        {"id": 110, "code_article": "C-B1", "libelle": "Étagère Bois B1", "pere": 11},
        {"id": 111, "code_article": "C-B2", "libelle": "Boite aux lettres", "pere": 10},
        
        # Niveau 3 : Les Livres (parent = Casiers)
        {"id": 1001, "code_article": "LIV-01", "libelle": "Manuel de Python", "pere": 100},
        {"id": 1002, "code_article": "LIV-02", "libelle": "Algorithmique Avancée", "pere": 100},
        {"id": 1011, "code_article": "LIV-03", "libelle": "Architecture Réseaux", "pere": 101},
        {"id": 1101, "code_article": "LIV-04", "libelle": "Histoire de l'Art", "pere": 110},

        # Niveau 3? : Les Livres qui n'ont pas encore de casier (parent = Salle)
        {"id": 1110, "code_article": "LIV-05", "libelle": "Guide de la Lecture", "pere": 111 },
        {"id": 1111, "code_article": "LIV-06", "libelle": "Guide du voyageur intergalactique", "pere": 111 },
    
    ]

    mon_arbre = ArticleTree()
    mon_arbre.ajouter_depuis_liste(donnees_articles)
    
    print("Inventaire Hiérarchique du Bâtiment :\n")
    # On commence par le sommet de la pyramide (pere is None)
    mon_arbre.afficher_arbre(parent_id=None)