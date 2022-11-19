import random
import numpy as np


# Retourne un tableau vide
def init_tableau(largeur, longeur):
    return np.zeros([largeur, longeur], dtype=float)


# Met a jour la proba d'une case
def mise_a_jour_proba(proba_ps, proba_pi_i, proba_pi_k):
    pi_i = proba_pi_k / (1 - proba_ps * proba_pi_i)
    return pi_i


# Met à jour l'ensemble du tableau
def mise_a_jour_tableau_proba(plateau_proba_ps, plateau_proba_pi, proba_pi_k):
    for i in range(0, len(plateau_proba_ps)):
        for j in range(0, len(plateau_proba_ps[0])):
            plateau_proba_pi[i, j] = mise_a_jour_proba(plateau_proba_ps[i, j], plateau_proba_pi[i, j], proba_pi_k)


# Retourne la case où il est le plus probable de trouver l'objet recherché
def meilleur_position(plateau):
    nb_max = -1
    meilleur_pos = [0, 0]
    for i in range(0, len(plateau)):
        for j in range(0, len(plateau[0])):
            if plateau[i, j] > nb_max:
                nb_max = plateau[i, j]
                meilleur_pos[0] = i
                meilleur_pos[1] = j

    return meilleur_pos


# Initialise les tableaux nécessaires pour l'algorithme de senseur_imparfait
def init_plateaux(largeur, longeur, rand, tableau_proba_ps, tableau_proba_pi):
    if rand == 1:
        plateau_proba_ps = init_tableau(largeur, longeur)
        plateau_proba_pi = init_tableau(largeur, longeur)
        for i in range(largeur):
            for j in range(longeur):
                proba = random.uniform(0, 1)
                plateau_proba_ps[i, j] = proba
                plateau_proba_pi[i, j] = proba
    else:
        plateau_proba_ps = np.copy(tableau_proba_ps)
        plateau_proba_pi = np.copy(tableau_proba_pi)

    return [plateau_proba_ps, plateau_proba_pi]


# Algorithme de senseur_imparfait
def senseur_imparfait(largeur, longeur, rand, position_objet, tableau_proba_ps, tableau_proba_pi):
    compteur = 0
    trouver = False
    tableau = init_plateaux(largeur, longeur, rand, tableau_proba_ps, tableau_proba_pi)
    plateau_proba_ps = tableau[0]
    plateau_proba_pi = tableau[1]

    if rand == 1:
        position_cache = [random.randint(0, largeur - 1), random.randint(0, longeur - 1)]
    else:
        position_cache = [position_objet[0], position_objet[1]]

    while not trouver:
        position = meilleur_position(plateau_proba_pi)

        if position[0] == position_cache[0] and position[1] == position_cache[1]:
            temp = random.random()
            if temp <= plateau_proba_ps[position_cache[0], position_cache[1]]:
                trouver = True
        else:
            mise_a_jour_tableau_proba(plateau_proba_ps, plateau_proba_pi, plateau_proba_pi[position[0], position[1]])

        compteur += 1

    return compteur
