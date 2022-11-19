import numpy as np
from Bataille import *
from Bateau import *


# La fonction retourne True si la case de position donnée est libre et False sinon
def case_libre(grille, position):
    return grille[position.x, position.y] == 0


# La fonction retourne True si les cases avec les coordonnées données sont libre et False sinon
def cases_libres(grille, x1, x2, y1, y2):
    # On teste la sous-matrice qui correspond aux cases selectionnées
    # Si toutes les cases ne sont pas égales à 0, alors il existe une case occupée
    return (grille[x1:x2, y1:y2] == 0).all()


# La fonction retourne True si la case de position sélectionnée déborde du plateau et False sinon
def depassement_plateau(x, taille_bateau, taille_plateau):
    return x + taille_bateau > taille_plateau


# Paramètres : list[10][10]* Bateau * tuple(int*int) * int --> bool
# La fonction retoure True si le joueur peut placer le bateau à la position sélectionnée et False sinon
# Par defaut, on commence d'en haut vers le bas et de gauche vers la droite.
def peut_placer(grille, bateau, position, direction):
    # Test si la position est libre
    if not case_libre(grille, position):
        return False

    # Test si la direction souhaitée est verticale
    elif direction == 1:
        # Test que le bateau ne sort pas de la grille verticalement
        if depassement_plateau(position.x, bateau.taille, len(grille)):
            return False
        # Test que les futures cases du bateau soient libres
        if not cases_libres(grille, position.x, position.x + bateau.taille, position.y, position.y + 1):
            return False

        # Test si la direction souhaitée est horizontale
    else:  # direction == 2
        # Test que le bateau ne sort pas de la grille horizontalement
        if depassement_plateau(position.y, bateau.taille, len(grille)):
            return False
        # Test que les futures cases du bateau soient libres
        if not cases_libres(grille, position.x, position.x + 1, position.y, position.y + bateau.taille):
            return False

    return True


# Fonction qui place le bateau si possible et retourne la grille modifée où le bateau a été placé comme indiqué
def place(grille, bateau, position, direction):
    if peut_placer(grille, bateau, position, direction):
        # Test si la direction souhaitée est verticale
        if direction == 1:
            for i in range(position.x, position.x + bateau.taille):
                grille[i, position.y] = bateau.identifiant

        # Test si la direction souhaitée est horizontale
        else:  # Direction = 2 :
            for i in range(position.y, position.y + bateau.taille):
                grille[position.x, i] = bateau.identifiant


# Place aléatoirement le bateau dans la grille en tirant uniformément une position et une direction aléatoires
# jusqu'à ce que le positionnement choisi soit admissible et effectué
def place_alea(grille, bateau):
    position = Position(bateau.identifiant, random.randint(0, len(grille) - 1), random.randint(0, len(grille[0]) - 1))
    direction = random.randint(1, 2)

    while not peut_placer(grille, bateau, position, direction):
        position = Position(bateau.identifiant, random.randint(0, len(grille) - 1),
                            random.randint(0, len(grille[0]) - 1))
        direction = random.randint(1, 2)

    place(grille, bateau, position, direction)


# Affiche la grille du jeu
def affiche(grille):
    print("---------------------------------------")
    print(grille)


# Permet de tester l'égalité entre 2 grilles
def egalite_grilles(grille_a, grille_b):
    return np.array_equal(grille_a, grille_b)


# Génère des bateaux
def genere_bateaux(liste_identidiant, liste_taille):
    bateaux = []
    for i in range(len(liste_identidiant)):
        bateaux.append(Bateau(liste_identidiant[i], liste_taille[i]))
    return bateaux


# Génère une grille comprenant l'ensemble des bateaux du jeu disposés de manière aléatoire
def genere_grille(largeur_plateau, longeur_plateau, bateaux):
    plateau = np.zeros((largeur_plateau, longeur_plateau), dtype=int)

    for bateau in bateaux:
        place_alea(plateau, bateau)

    return plateau


# Calcule le nombre de façons de placer un bateau donnée sur une grille vide
# exo 2 - question 2
def calcul_nombre_facon(taille_bateau, longeur_plateau, largeur_plateau):
    compteur = 0
    compteur_longeur = 0
    compteur_largeur = 0

    # Nombre de position sur une largeur
    for i in range(0, largeur_plateau):
        if not depassement_plateau(i, taille_bateau, largeur_plateau):
            compteur_largeur += 1
        else:
            break
    # Nombre de position sur toutes les largeurs
    compteur += compteur_largeur * longeur_plateau

    # Nombre de position sur une longueur
    for i in range(0, longeur_plateau):
        if not depassement_plateau(i, taille_bateau, longeur_plateau):
            compteur_longeur += 1
        else:
            break
    # Nombre de position sur toutes les longueurs
    compteur += compteur_longeur * largeur_plateau

    return compteur


# Calcul le nombre de facon pour une liste 3 bateaux
# exo 2 - question 3
def calcul_nombre_facon_liste3(plateau, bateaux):
    resultat = []
    plateau = init_tableau(len(plateau), len(plateau[0]))
    # On ajoute pour chaque bateau toutes les cases possibles
    for bateau in bateaux:
        resultat.append(calcul_cas_possible_position(plateau, bateau))

    compteur1 = 0
    compteur2 = 0

    # Vertical
    # On parcourt la liste qui contient les listes de deplacement possible pour chaque bateau
    for i in resultat[0]:
        # On place le premier bateau s'il est placable
        # On utilise le premier element de la liste qui correspondàa la premiere position pour savoir s'il est placable
        if peut_placer(plateau, bateaux[0], i[0], 1):
            # On selectionne les cases où on place le bateaux
            temp1 = ajoute_case_vertical(i[0].x, i[0].y, bateaux[0])
            modifie_grille(plateau, temp1, -1)
            # On place le deuxieme bateaux s'il est placable
            for j in resultat[1]:
                if peut_placer(plateau, bateaux[1], j[0], 1):
                    # selectionne les cases où on place le bateau
                    temp2 = ajoute_case_vertical(j[0].x, j[0].y, bateaux[1])
                    # on modifie la grille en placant les cases à -1
                    modifie_grille(plateau, temp2, -1)
                    # On place le troisieme bateau s'il est placable
                    for k in resultat[2]:
                        if peut_placer(plateau, bateaux[2], k[0], 1):
                            # Si on peut placer le dernier bateau, alors on incremente
                            # si on incrémentenle compteur, alors il existe une grille supplémentaire
                            compteur1 += 1

                    # on replace les bateaux pour le prochain bateau
                    modifie_grille(plateau, temp2, 0)
            modifie_grille(plateau, temp1, 0)

    # Horizontal
    for i in resultat[0]:

        if peut_placer(plateau, bateaux[0], i[0], 2):
            temp1 = ajoute_case_horizontal(i[0].x, i[0].y, bateaux[0])
            modifie_grille(plateau, temp1, -1)
            for j in resultat[1]:
                if peut_placer(plateau, bateaux[1], j[0], 2):
                    temp2 = ajoute_case_horizontal(j[0].x, j[0].y, bateaux[1])
                    modifie_grille(plateau, temp2, -1)
                    for k in resultat[2]:
                        if peut_placer(plateau, bateaux[2], k[0], 2):
                            compteur2 += 1

                    modifie_grille(plateau, temp2, 0)
            modifie_grille(plateau, temp1, 0)

    return compteur1 + compteur2


# Calcul le nombre de facon pour une liste de 2 bateaux
# exo 2 - question 3
def calcul_nombre_facon_liste2(plateau, bateaux):
    resultat = []
    plateau = init_tableau(len(plateau), len(plateau[0]))
    # On ajoute pour chaque bateau toute les cases possibles
    for bateau in bateaux:
        resultat.append(calcul_cas_possible_position(plateau, bateau))

    compteur1 = 0
    compteur2 = 0

    # Vertical
    # On parcourt la liste qui contient les listes de deplacement possible pour chaque bateau
    for i in resultat[0]:
        # On place le premier bateaux s'il est placable
        # On utilise le premier element de la liste qui correspond à la premiere position pour savoir s'il est placable
        if peut_placer(plateau, bateaux[0], i[0], 1):
            # On selectionne les cases où on place le bateaux
            temp1 = ajoute_case_vertical(i[0].x, i[0].y, bateaux[0])
            modifie_grille(plateau, temp1, -1)
            # On place le deuxieme bateaux s'il est placable
            for k in resultat[1]:
                if peut_placer(plateau, bateaux[1], k[0], 1):
                    # Si on peut placer le dernier bateau, alors on incremente
                    # si on incrémentenle compteur, alors il existe une grille supplémentaire
                    compteur1 += 1

            # on replace les bateaux pour le prochain bateau
            modifie_grille(plateau, temp1, 0)

    # Horizontal
    for i in resultat[0]:

        if peut_placer(plateau, bateaux[0], i[0], 2):
            temp1 = ajoute_case_horizontal(i[0].x, i[0].y, bateaux[0])
            modifie_grille(plateau, temp1, -1)
            for k in resultat[1]:
                if peut_placer(plateau, bateaux[1], k[0], 2):
                    compteur2 += 1

            modifie_grille(plateau, temp1, 0)

    return compteur1 + compteur2


# Calcul le nombre de grilles pour un bateau orienté horizontalement
def calcul_nombre_facon_horizontal(taille_bateau, longeur_plateau, largeur_plateau):
    compteur_largeur = 0

    # Nombre de position sur une largeur
    for i in range(0, largeur_plateau):
        if not depassement_plateau(i, taille_bateau, largeur_plateau):
            compteur_largeur += 1
        else:
            break
    # Nombre de position sur toutes les largeurs
    return compteur_largeur * longeur_plateau


# Calcul le nombre de grilles pour un bateau orienté verticalement
def calcul_nombre_facon_vertical(taille_bateau, longeur_plateau, largeur_plateau):
    compteur_longeur = 0
    # Nombre de position sur une longueur
    for i in range(0, longeur_plateau):
        if not depassement_plateau(i, taille_bateau, longeur_plateau):
            compteur_longeur += 1
        else:
            break
    # Nombre de position sur toutes les longueurs
    return compteur_longeur * largeur_plateau


# Calcul approximative du nombre total de grilles pour une liste complète de bateaux
# exo 2 - question 6
def approximation_nombre_total_grille_ameliorer():
    # bateau de taille5
    bateau1 = calcul_nombre_facon(5, 10, 10)
    print("nb config pour un porte-avions (taille 5) : {}".format(bateau1))
    # bateau de taille4
    bateau2 = calcul_nombre_facon_vertical(4, 10, 9) + calcul_nombre_facon_horizontal(4, 9, 10) \
              + calcul_nombre_facon_vertical(4, 5, 1) + calcul_nombre_facon_horizontal(4, 1, 5)
    print("nb config pour un croiseur (taille 4) : {}".format(bateau2))
    # bateau de taille3
    bateau3 = calcul_nombre_facon_vertical(3, 9, 9) + calcul_nombre_facon_horizontal(3, 10, 9) \
              + calcul_nombre_facon_vertical(3, 10, 1)
    print("nb config pour un contre-torpilleurs (taille 3) : {}".format(bateau3))
    # bateau de taille3
    bateau4 = calcul_nombre_facon_vertical(3, 9, 9) + calcul_nombre_facon_horizontal(3, 10, 8) \
              + calcul_nombre_facon_vertical(3, 7, 1) + calcul_nombre_facon_horizontal(3, 1, 7)
    print("nb config pour un sous-marin (taille 3) : {}".format(bateau4))
    # bateau de taille2
    bateau5 = calcul_nombre_facon_horizontal(2, 1, 4) + calcul_nombre_facon_horizontal(2, 8, 10) \
              + calcul_nombre_facon_vertical(2, 9, 9) + calcul_nombre_facon_vertical(2, 4, 1)
    print("nb config pour un torpilleur (taille 2) : {} \n".format(bateau5))

    produit = bateau1 * bateau2 * bateau3 * bateau4 * bateau5
    print("nb config total : {}".format(produit))

    return produit


# Ajoute les cases de (i, j) à (i+bateau.taille, j) et la retourne
def ajoute_case_vertical(i, j, bateau):
    temp = []
    for k in range(i, i + bateau.taille):
        temp.append(Position(bateau.id, k, j))
    return temp


# Ajoute les cases de (i, j) à (i, j+bateau.taille) dans une liste et la retourne
def ajoute_case_horizontal(i, j, bateau):
    temp = []
    for k in range(j, j + bateau.taille):
        temp.append(Position(bateau.id, i, k))
    return temp


# Fonction qui retourne le bateau d'identifaint id_bateau
def retourne_bateau(bateaux, id_bateau):
    for bateau in bateaux:
        if bateau.id == id_bateau:
            return bateau
    return None


# Modifie la grille avec les paramètres souhaités
def modifie_grille(grille, positions, valeur):
    for position in positions:
        grille[position.x, position.y] = valeur


# Fonction qui prend en parametre une grille et qui retourne le nombre d'essais avant de tomber sur la meme grille
# exo 2 - question 4
def calcul_egalite_grille(grille_a, bateaux):
    largeur_grille = len(grille_a[0])
    longeur_grille = len(grille_a)
    grille_b = genere_grille(largeur_grille, longeur_grille, bateaux)
    compteur = 1
    while not egalite_grilles(grille_a, grille_b):
        compteur += 1
        grille_b = genere_grille(largeur_grille, longeur_grille, bateaux)

    return compteur


# La fonction retourne True si les cases de position sélectionnée sont libres et False sinon
def cases_libres_proba(grille, x1, x2, y1, y2):
    # On test la sous-matrice qui correspond au cases selectionnées
    # S'il existe une case égale a -1, alors on ne peut pas placer le bateau
    return (grille[x1:x2, y1:y2] == -1).any()


# Fonction qui retourne True si on peut place le bateau sur une postion et orientation données, False sinon
def peut_placer_proba(grille, bateau, position, direction):
    # Test si la direction souhaitée est verticale
    if direction == 1:
        # Test que le bateau ne sort pas de la grille verticalement
        if depassement_plateau(position.x, bateau.taille, len(grille)):
            return False
        # Test que les futures cases du bateau soient libres
        if cases_libres_proba(grille, position.x, position.x + bateau.taille, position.y, position.y + 1):
            return False

    # Test si la direction souhaitée est horizontale
    else:  # direction == 2
        # Test que le bateau ne sort pas de la grille horizontalement
        if depassement_plateau(position.y, bateau.taille, len(grille)):
            return False
        # Test que les futures cases du bateau soient libres
        if cases_libres_proba(grille, position.x, position.x + 1, position.y, position.y + bateau.taille):
            return False

    return True


# Retourne un tableau vide
def init_tableau(largeur, longeur):
    return np.zeros([largeur, longeur], dtype=int)


# Calcul les differents cas possible pour chaque bateau
# et retourne une liste contenant des listes de positions où on peut placer le bateau
def calcul_cas_possible_position(plateau, bateau):
    position = []
    for i in range(0, len(plateau)):
        for j in range(0, len(plateau[0])):
            if peut_placer_proba(plateau, bateau, Position(plateau[i, j], i, j), 1):
                temp = []
                for k in range(i, i + bateau.taille):
                    temp.append(Position(bateau.identifiant, k, j))
                position.append(temp)

            if peut_placer_proba(plateau, bateau, Position(plateau[i, j], i, j), 2):
                temp = []
                for k in range(j, j + bateau.taille):
                    temp.append(Position(bateau.identifiant, i, k))
                position.append(temp)
    return position
