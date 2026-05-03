"""
Dans cette implémentation, nous avons défini une classe `Noeud` qui représente 
un noeud dans une arborescence.

Chaque noeud a :
- un identifiant (`id`),
- un libellé (`libelle`)
- un père (`pere`) qui est un autre noeud ou `None` s'il n'a pas de père comme la racine de l'arbre.

La méthode `CreerArbre` permet de construire une arborescence à partir d'une liste de dictionnaires, 
où le premier élément est l'identifiant, le deuxième est le libellé, 
et l'élément précédent est le père'.
"""

class ArticleNode:
    """
    Représente un nœud dans l'arbre des articles sans redondance.
    """
    def __init__(self, id, code_article, libelle, pere=None, tag=[]):
        self.id = id
        self.code_article = code_article
        self.libelle = libelle
        self.pere = pere  # ID du parent (unique lien de parenté)
        self.tag = tag # Liste de tags pour les annotations supplémentaires

    def __repr__(self):
        return f"Noeud({self.code_article}: {self.libelle})"


class ArticleTree:
    """
    Gère la hiérarchie des articles en utilisant uniquement l'attribut 'pere'.
    """
    def __init__(self):
        self.nodes = {}  # Stockage à plat des noeuds par ID

    def ajouter_depuis_liste(self, liste_articles):
        """
        Remplit le dictionnaire de noeuds à partir d'une liste brute.
        """
        for item in liste_articles:
            # Creation d'un objet de type noeud
            noeud = ArticleNode(
                id = item['id'],
                code_article = item['code_article'],
                libelle = item['libelle'],
                pere = item['pere'],
                tag = item['tag']
            )
            # Ajoute de cet objet à l'arbre dico pour clé 'id'
            self.nodes[noeud.id] = noeud
            

    def trouver_enfants(self, parent_id):
        """
        Recherche dynamiquement tous les noeuds ayant un parent spécifique.
        """
        return [node for node in self.nodes.values() if node.pere == parent_id]

    def trouver_chemin(self, id_destination):
        """
        Remonte l'arbre de l'enfant vers la racine pour construire le chemin.
        """
        chemin = []
        courant_id = id_destination

        while courant_id is not None:
            noeud = self.nodes[courant_id]
            if noeud:
                chemin.append(noeud)
                courant_id = noeud.pere
            else:
                break
        
        # On inverse la liste pour l'avoir de la racine vers la destination
        return chemin[::-1]


    def afficher_arbre(self, parent_id=None, niveau=0):
        """
        Affiche l'arbre de manière récursive en filtrant par l'ID du père.
        """
        # On récupère les noeuds qui ont parent_id comme père
        enfants = self.trouver_enfants(parent_id)
        
        for n in enfants:
            indentation = "  " * niveau
            prefixe = "└── " if niveau > 0 else "• "
            print(f"{indentation}{prefixe}[{n.code_article}] {n.libelle}")
            
            # Appel récursif pour chercher les enfants de ce nœud
            self.afficher_arbre(n.id, niveau + 1)

    def afficher_orphelin(self):
        """
        Affiche les noeuds non associés (0)
        """
        print('Les articles non associés :')
        noeuds = self.nodes
        for noeud in noeuds.values():
            if noeud.pere == 0:
                print(f'{noeud}')          

    def ajouterTag(self, id, tag):
        """
        Ajoute un tag à la liste de tags du nœud identifié par 'id'.
        """
        if id in self.nodes:
            self.nodes[id].tag.append(tag)

    def sauvegarder_json(self, fichier):
        """
        Sauvegarde les noeuds de l'arbre dans un fichier JSON.
        """
        import json
        data = {node.id: {
            'code_article': node.code_article,
            'libelle': node.libelle,
            'pere': node.pere,
            'tag': node.tag
        } for node in self.nodes.values()}
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def charger_depuis_json(self, fichier):
        """
        Charge les noeuds depuis un fichier JSON et les ajoute à l'arbre.
        """
        import json
        
        with open(fichier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for node_id, node_data in data.items():
            node = ArticleNode(
                id = int(node_id),
                code_article = node_data['code_article'],
                libelle = node_data['libelle'],
                pere = node_data['pere'],
                tag = node_data['tag']
            )
            self.nodes[node.id] = node

if __name__ == "__main__":
    # Liste simulant la hiérarchie : Bâtiment > Salle > Casier > Livre
    
    donnees_articles = [
        # Niveau 0 : Le Bâtiment
        {"id": 1, "code_article": "BAT-A", "libelle": "Bâtiment Principal", "pere": None, "tag": ["Bâtiment"]},
        
        # Niveau 1 : Les Salles (parent = Bâtiment)
        {"id": 10, "code_article": "S01", "libelle": "Salle de Stockage Nord", "pere": 1, "tag": ["Salle"]},
        {"id": 11, "code_article": "S02", "libelle": "Salle de Lecture", "pere": 1, "tag": ["Salle"]},
        
        # Niveau 2 : Les Casiers (parent = Salles)
        {"id": 100, "code_article": "C-A1", "libelle": "Casier Métallique A1", "pere": 10, "tag": ["Casier"]},
        {"id": 101, "code_article": "C-A2", "libelle": "Casier Métallique A2", "pere": 10, "tag": ["Casier"]},
        {"id": 110, "code_article": "C-B1", "libelle": "Étagère Bois B1", "pere": 11, "tag": ["Casier"]},
        {"id": 111, "code_article": "C-B2", "libelle": "Boite aux lettres", "pere": 1, "tag": ["Arrivée"]},
        
        # Niveau 3 : Les Livres (parent = Casiers)
        {"id": 1001, "code_article": "LIV-01", "libelle": "Manuel de Python", "pere": 100, "tag": ["Livre"]},
        {"id": 1002, "code_article": "LIV-02", "libelle": "Algorithmique Avancée", "pere": 100, "tag": ["Livre"]},
        {"id": 1011, "code_article": "LIV-03", "libelle": "Architecture Réseaux", "pere": 101, "tag": ["Livre"]},
        {"id": 1101, "code_article": "LIV-04", "libelle": "Histoire de l'Art", "pere": 110, "tag": ["Livre"]},

        # Niveau 3? : Les Livres qui n'ont pas encore de casier (parent = Salle)
        {"id": 1110, "code_article": "LIV-05", "libelle": "Guide de la Lecture", "pere": 0, "tag": ["Livre"]},
        {"id": 1111, "code_article": "LIV-06", "libelle": "Guide du voyageur intergalactique", "pere": 0, "tag": ["Livre"]},
    
    ]

    mon_arbre = ArticleTree()
    mon_arbre.ajouter_depuis_liste(donnees_articles)
    
    print("Inventaire Hiérarchique du Bâtiment :\n")
    # On commence par le sommet de la pyramide (pere is None)
    mon_arbre.afficher_arbre(parent_id=None)

    print("-" * 30)
    
    # Interaction avec l'utilisateur
    try:
        id_cible = int(input("\nEntrez l'ID du nœud de destination pour trouver son chemin : "))
        
        if id_cible in mon_arbre.nodes:
            chemin = mon_arbre.trouver_chemin(id_cible)
            print(f"\nChemin trouvé pour arriver à '{mon_arbre.nodes[id_cible].libelle}' :")
            
            # Affichage formaté du chemin : Racine > ... > Cible
            noms_chemin = [str(n) for n in chemin]
            print(" > ".join(noms_chemin))
        else:
            print(f"Erreur : L'ID {id_cible} n'existe pas dans l'inventaire.")
            
    except ValueError:
        print("Erreur : Veuillez entrer un nombre entier pour l'ID.")
    
    # Sauvegarde de l'arbre dans un fichier JSON
    mon_arbre.sauvegarder_json("inventaire_batiment.json")
    print("\nL'inventaire a été sauvegardé dans 'inventaire_batiment.json'.")

    # Chargement de l'arbre depuis le fichier JSON pour vérification
    nouvel_arbre = ArticleTree()
    nouvel_arbre.charger_depuis_json("inventaire_batiment.json")
    print("\nArbre chargé depuis le fichier JSON :\n")
    nouvel_arbre.afficher_arbre(parent_id=None)
