class Bateau:  # Définition de notre classe Bateau
    """
    Classe définissant un bateau caractérisée par :
    - son id
    - sa taille
    - son nombre de vie restante
    """

    def __init__(self, identifiant, taille):  # Notre méthode constructeur
        self.identifiant = identifiant
        self.taille = taille
        self.vie = taille
