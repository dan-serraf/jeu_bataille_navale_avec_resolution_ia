class Position:  # Définition de notre classe Position
    """
    Classe définissant une position caractérisée par :
    - son id #Pour reset une grille on mémorise sa case
    - sa coordonné horizontale
    - sa coordonné verticale
    """

    def __init__(self, identifiant, x, y):  # Notre méthode constructeur
        self.identifiant = identifiant
        self.x = x
        self.y = y
