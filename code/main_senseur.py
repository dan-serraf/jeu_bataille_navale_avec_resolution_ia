import time
import numpy as np
from GenereGrille import *
from senseur_imparfait import *

compteur = 0
temps_total = 0

n = 100

largeur_plateau = 10
longeur_plateau = 10
rand = 0
position_objet = (4, 4)

tableau_proba_centre = np.array([[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                 [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                 [0.00, 0.00, 0.00, 0.00, 0.01, 0.02, 0.01, 0.01, 0.00, 0.00],
                                 [0.00, 0.00, 0.00, 0.10, 0.30, 0.20, 0.02, 0.03, 0.00, 0.00],
                                 [0.00, 0.01, 0.03, 0.06, 0.40, 0.08, 0.01, 0.02, 0.00, 0.00],
                                 [0.00, 0.60, 0.10, 0.08, 0.07, 0.20, 0.03, 0.03, 0.02, 0.00],
                                 [0.00, 0.30, 0.20, 0.10, 0.10, 0.06, 0.04, 0.04, 0.00, 0.00],
                                 [0.00, 0.00, 0.02, 0.05, 0.09, 0.04, 0.03, 0.00, 0.00, 0.00],
                                 [0.00, 0.00, 0.00, 0.01, 0.02, 0.01, 0.00, 0.00, 0.00, 0.00],
                                 [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]])

tableau_proba_bord = np.array([[0.10, 0.09, 0.08, 0.05, 0.08, 0.07, 0.00, 0.00, 0.00, 0.00],
                               [0.08, 0.20, 0.20, 0.10, 0.09, 0.06, 0.05, 0.04, 0.00, 0.00],
                               [0.30, 0.40, 0.10, 0.10, 0.08, 0.00, 0.00, 0.00, 0.00, 0.00],
                               [0.50, 0.20, 0.08, 0.09, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                               [0.08, 0.10, 0.06, 0.07, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01],
                               [0.05, 0.08, 0.05, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.05],
                               [0.03, 0.09, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.10],
                               [0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.05, 0.10],
                               [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.04, 0.08, 0.10],
                               [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02, 0.09, 0.10]])

tableau_proba = np.copy(tableau_proba_centre)
tableau_proba_ps = np.copy(tableau_proba)
tableau_proba_pi = np.copy(tableau_proba)

bateaux = genere_bateaux([1], [5])
plateau = genere_grille(10, 10, bateaux)
tableau_occurence = np.zeros(100000, dtype=float)

for i in range(n):
    print("test numéro {}".format(i))

    tic = time.perf_counter()
    coups = senseur_imparfait(largeur_plateau, longeur_plateau, rand,
                              position_objet, tableau_proba_ps, tableau_proba_pi)
    toc = time.perf_counter()

    for k in range(0, len(tableau_occurence)):
        if k == coups:
            tableau_occurence[k] += 1

    if coups > len(tableau_occurence):
        print(coups)

    temps = toc - tic
    # print("{} coups en {} s\n".format(coups, temps))

    compteur = compteur + coups
    temps_total = temps_total + temps

moyenne_essais = compteur / n
moyenne_temps = temps_total / n
print("nb coups moyen : {}".format(moyenne_essais))
print("temps moyen : {} s".format(moyenne_temps))
print("tableau_occurence")
for k in range(0, len(tableau_occurence)):
    if tableau_occurence[k] != 0:
        print("{} coups en {} fois".format(k, tableau_occurence[k]))
