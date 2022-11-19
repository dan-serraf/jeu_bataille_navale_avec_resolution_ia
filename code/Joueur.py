import numpy as np
import random
from GenereGrille import *


class Joueur:  # Définition de notre classe Joueur
    """
    Classe définissant un bateau caractérisée par :
    - sa position
    """

    def __init__(self, position):  # Notre méthode constructeur
        self.position = position

    def liste_position(self, longeur, largeur):
        positions = []
        for i in range(longeur):
            for j in range(largeur):
                positions.append((i, j))
        random.shuffle(positions)
        return positions

    def tire_position_aleatoire(self, liste_position):
        if len(liste_position) > 0:
            position = liste_position[len(liste_position) - 1]
            liste_position.pop()
            return position

    def tire_position_probabiliste(self, bataille):
        bataille.calcule_proba(bataille.bateaux)
        return bataille.meilleur_position()

    def tire_position_monte_carlo(self, bataille, nombre_iteration):
        bataille.calcule_monte_carlo(nombre_iteration)
        return bataille.meilleur_position()

    def joue_aleatoire(self, bataille, liste_position):
        while not bataille.victoire():
            position = self.tire_position_aleatoire(liste_position)
            bataille.touche_aleatoire(Position(bataille.plateau[position[0], position[1]], position[0], position[1]))
        return bataille.compteur

    def joue_heuristique(self, bataille, liste_position):
        while not bataille.victoire():
            position = self.tire_position_aleatoire(liste_position)
            bataille.touche_heuristique(Position(bataille.plateau[position[0], position[1]], position[0], position[1]),
                                        liste_position)
        return bataille.compteur

    def joue_probabiliste(self, bataille, liste_position):
        while not bataille.victoire():
            bataille.tableau_proba = init_tableau(len(bataille.plateau), len(bataille.plateau[0]))
            position = self.tire_position_probabiliste(bataille)
            bataille.touche_probabiliste(Position(bataille.plateau[position[0], position[1]], position[0], position[1]),
                                         liste_position)
        return bataille.compteur

    def joue_monte_carlo(self, bataille, liste_position):
        while not bataille.victoire():
            bataille.tableau_proba = init_tableau(len(bataille.plateau), len(bataille.plateau[0]))
            position = self.tire_position_monte_carlo(bataille, 20000)
            bataille.touche_monte_carlo(Position(bataille.plateau[position[0], position[1]], position[0], position[1]),
                                        liste_position)
        return bataille.compteur
