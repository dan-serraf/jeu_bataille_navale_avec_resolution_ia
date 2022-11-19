import numpy as np
import random
import copy
from Position import *
from GenereGrille import *


class Bataille:  # Définition de notre classe Bataille
    """
    Classe définissant une bataille caractérisée par :
    - un plateau
    - des méthodes
    """

    def __init__(self, plateau, bateaux):  # Notre méthode constructeur
        self.plateau = plateau
        self.tableau_proba = np.zeros([len(plateau), len(plateau[0])], dtype=int)
        self.position_jouer = []
        self.position_toucher = []
        self.bateaux = bateaux
        self.bateaux_ref = copy.deepcopy(bateaux)
        self.plateau_ref = copy.deepcopy(plateau)
        self.compteur = 0

    # méthode aleatoire
    def touche_aleatoire(self, position):
        # Si la case n'a pas encore été jouée, alors elle est différente de -1
        if self.plateau[position.x, position.y] != -1:
            # Si la case n'a pas encore été visitée, alors elle est différente de 0
            if self.plateau[position.x, position.y] != 0:
                # Dans ce cas, la case est forcement un bateau
                self.position_toucher.append(Position(position.identifiant, position.x, position.y))
                self.diminue_vie(position.identifiant)

        # On met la case à -1
        self.plateau[position.x, position.y] = -1
        # On ajoute la position
        self.position_jouer.append(Position(0, position.x, position.y))
        self.compteur += 1

    # méthode heuristique
    def touche_heuristique(self, position, liste_position):
        # Si la case n'a pas encore été jouée elle est différente de -1
        if self.plateau[position.x, position.y] != -1:
            # Si la case n'a pas encore été visitée elle est différente de 0
            if self.plateau[position.x, position.y] != 0:
                # Dans ce cas, la case est forcement un bateau
                self.position_toucher.append(position)
                self.diminue_vie(position.identifiant)
                self.case_connexe(self.retourne_bateau(self.bateaux, self.plateau[position.x, position.y]), position,
                                  liste_position)

        # On met la case à -1
        self.plateau[position.x, position.y] = -1
        # On ajoute la position
        self.position_jouer.append(Position(0, position.x, position.y))
        self.compteur += 1

    # Test les cases en horizontal puis en vertical une fois qu'une case touchée
    def case_connexe(self, bateau, position, liste_position):
        position2 = Position(bateau.identifiant, position.x, position.y)

        # gauche
        position2.x = position.x
        position2.y = position.y - 1
        self.case_connexe_horizontal(bateau, position2, -1, liste_position)

        # droite
        position2.x = position.x
        position2.y = position.y + 1
        self.case_connexe_horizontal(bateau, position2, 1, liste_position)

        # haut
        position2.x = position.x - 1
        position2.y = position.y
        self.case_connexe_vertical(bateau, position2, -1, liste_position)

        # bas
        position2.x = position.x + 1
        position2.y = position.y
        self.case_connexe_vertical(bateau, position2, 1, liste_position)

    # Test les cases verticales
    def case_connexe_vertical(self, bateau, position, valeur, liste_position):
        # Test si la case est valide et si le bateau est en vie
        if 0 <= position.x < len(self.plateau[0]) and bateau.vie > 0:
            # Si on touche le bateau on enleve une vie
            if self.plateau[position.x, position.y] == bateau.identifiant:
                self.position_toucher.append(position)
                self.position_jouer.append(Position(bateau.identifiant, position.x, position.y))
                self.diminue_vie(bateau.identifiant)
                self.supprimer_position((position.x, position.y), liste_position)
                self.plateau[position.x, position.y] = -1
                self.compteur += 1
                position.x = position.x + valeur
                self.case_connexe_vertical(bateau, position, valeur, liste_position)

            # Si la case a deja été visitée, alors on passe
            elif self.plateau[position.x, position.y] == -1:
                pass

            # Si la case n'a pas été visitée, alors on la visite
            elif self.plateau[position.x, position.y] == 0:
                self.plateau[position.x, position.y] = -1
                self.position_jouer.append(Position(0, position.x, position.y))
                self.supprimer_position((position.x, position.y), liste_position)
                self.compteur += 1

            # Sinon
            else:  # on a touché un autre bateau
                pass

    # Test les cases horizontales
    def case_connexe_horizontal(self, bateau, position, valeur, liste_position):
        # Test si la case est valide et si le bateau est en vie
        if 0 <= position.y < len(self.plateau) and bateau.vie > 0:
            # Si on touche le bateau, alors on enleve une vie
            if self.plateau[position.x, position.y] == bateau.identifiant:
                self.position_toucher.append(position)
                self.position_jouer.append(Position(bateau.identifiant, position.x, position.y))
                self.diminue_vie(bateau.identifiant)
                self.supprimer_position((position.x, position.y), liste_position)
                self.plateau[position.x, position.y] = -1
                self.compteur += 1
                position.y = position.y + valeur
                self.case_connexe_horizontal(bateau, position, valeur, liste_position)

            # Si la case a deja été visitée, alors on passe
            elif self.plateau[position.x, position.y] == -1:
                pass

            # Si la case n'a pas été visitée, alors on la visite
            elif self.plateau[position.x, position.y] == 0:
                self.plateau[position.x, position.y] = -1
                self.position_jouer.append(Position(0, position.x, position.y))
                self.supprimer_position((position.x, position.y), liste_position)
                self.compteur += 1

            # Sinon
            else:  # on a touché un autre bateau
                pass

    # méthode probabiliste simplifiée
    def touche_probabiliste(self, position, liste_position):
        # Si la case n'a pas encore été jouée, alors elle est différente de -1
        if self.plateau[position.x, position.y] != -1:
            # Si la case n'a pas encore été visitée, alors elle est différente de 0
            if self.plateau[position.x, position.y] != 0:
                # Dans ce cas la case est forcement un bateau
                self.position_toucher.append(position)
                self.diminue_vie(position.identifiant)
                self.case_connexe(self.retourne_bateau(self.bateaux, self.plateau[position.x, position.y]), position,
                                  liste_position)

        # On met la case a -1
        self.plateau[position.x, position.y] = -1
        self.tableau_proba[position.x, position.y] = -1
        # On ajoute la position
        self.position_jouer.append(Position(0, position.x, position.y))
        self.compteur += 1

    # Retourne la position qui possede potentiellement le plus de chance de toucher un bateau
    def meilleur_position(self):
        nb_max = 0
        meilleur_position = [0, 0]
        for i in range(0, len(self.plateau)):
            for j in range(0, len(self.plateau[0])):
                if self.tableau_proba[i, j] > nb_max:
                    nb_max = self.tableau_proba[i, j]
                    meilleur_position[0] = i
                    meilleur_position[1] = j

        return meilleur_position

    # Calcul les probabilités de toucher un bateau
    def calcule_proba(self, bateaux):
        for bateau in bateaux:
            if bateau.vie > 0:
                self.calcul_cas_possible(bateau, len(self.plateau), len(self.plateau[0]))

    # La fonction retourne True si les cases de position sélectionner sont libre et False sinon
    def cases_libres_proba(self, grille, x1, x2, y1, y2):
        # On test la sous matrice qui correspond au cases selectionner
        # S'il existe une case égale a -1 alors on ne peut pas placer le bateau on revoit False et True sinon
        return (grille[x1:x2, y1:y2] == -1).any()

    # La fonction retourne True si la case de position sélectionner déborde du plateau et False sinon
    def depassement_plateau(self, x, taille_bateau, taille_plateau):
        return x + taille_bateau > taille_plateau

    def peut_placer_proba(self, grille, bateau, position, direction):

        # Test si la direction souhaitée est verticale
        if direction == 1:
            # Test que le bateau ne sort pas de la grille verticalement
            if self.depassement_plateau(position.x, bateau.taille, len(grille)):
                return False
            # Test que les futures cases du bateau soient libres
            if self.cases_libres_proba(grille, position.x, position.x + bateau.taille, position.y, position.y + 1):
                return False

            # Test si la direction souhaitée est horizontale
        else:  # direction == 2
            # Test que le bateau ne sort pas de la grille horizontalement
            if self.depassement_plateau(position.y, bateau.taille, len(grille)):
                return False
            # Test que les futures cases du bateau soient libres
            if self.cases_libres_proba(grille, position.x, position.x + 1, position.y, position.y + bateau.taille):
                return False

        return True

    # Calcul les differents cas possible pour chaque bateau
    # et retourne une liste contenant des listes de positions où peut etre place "bateau"
    def calcul_cas_possible_position(self, plateau, bateau):
        position = []
        for i in range(0, len(plateau)):
            for j in range(0, len(plateau[0])):
                if self.peut_placer_proba(plateau, bateau, Position(plateau[i, j], i, j), 1):
                    temp = []
                    for k in range(i, i + bateau.taille):
                        temp.append(Position(bateau.identifiant, k, j))
                    position.append(temp)

                if self.peut_placer_proba(plateau, bateau, Position(plateau[i, j], i, j), 2):
                    temp = []
                    for k in range(j, j + bateau.taille):
                        temp.append(Position(bateau.identifiant, i, k))
                    position.append(temp)
        return position

    # Calcul les differents cas possible pour chaque bateau et modifie le tableau de probabilite
    def calcul_cas_possible(self, bateau, longeur_plateau, largeur_plateau):

        for i in range(0, largeur_plateau):
            for j in range(0, longeur_plateau):
                if self.peut_placer_proba(self.plateau, bateau, Position(self.plateau[i, j], i, j), 1):

                    for k in range(i, i + bateau.taille):
                        self.tableau_proba[k, j] += 1

                if self.peut_placer_proba(self.plateau, bateau, Position(self.plateau[i, j], i, j), 2):

                    for k in range(j, j + bateau.taille):
                        self.tableau_proba[i, k] += 1

    def touche_monte_carlo(self, position, liste_position):
        # Si la case n'a pas encore été jouée, alors elle est différente de -1
        if self.plateau[position.x, position.y] != -1:
            # Si la case n'a pas encore été visitée, alors elle est différente de 0
            if self.plateau[position.x, position.y] != 0:
                # Dans ce cas, la case est forcement un bateau
                self.position_toucher.append(position)
                self.diminue_vie(position.identifiant)
                self.case_connexe(retourne_bateau(self.bateaux, self.plateau[position.x, position.y]), position,
                                  liste_position)

        # On met la case à -1
        self.plateau[position.x, position.y] = -1
        self.tableau_proba[position.x, position.y] = -1
        # On ajoute la position
        self.position_jouer.append(Position(0, position.x, position.y))
        self.compteur += 1

    def calcule_monte_carlo(self, nombre_iteration):
        # initialise la grille
        plateau2 = self.init_tableau(len(self.plateau), len(self.plateau[0]))

        # ajoute les contraintes
        for position in self.position_jouer:
            self.modifie_grille(plateau2, position, -1)

        # genere les grilles
        self.monte_carlo(plateau2, self.bateau_vivant(), nombre_iteration)

    def monte_carlo(self, plateaux, bateaux, nombre_iteration):
        # liste cas possible par bateaux
        resultat = []

        # On ajoute pour chaque bateaux toute les cases possibles
        if type(bateaux) == list:
            for bateau in bateaux:
                resultat.append(self.calcul_cas_possible_position(plateaux, bateau))
            plateau2 = copy.deepcopy(plateaux)
            for k in range(nombre_iteration):
                temp = []
                for i in range(len(resultat)):
                    if len(resultat[i]) > 0:
                        indice = random.randint(0, len(resultat[i]) - 1)
                        if self.peut_placer_proba(plateau2, bateaux[i], resultat[i][indice][0], 1):
                            for position in resultat[i][indice]:
                                self.modifie_grille(plateau2, position, -1)
                                temp.append(position)
                                self.tableau_proba[position.x, position.y] += 1

                        if self.peut_placer_proba(plateau2, bateaux[i], resultat[i][indice][0], 2):
                            for position in resultat[i][indice]:
                                self.modifie_grille(plateau2, position, -1)
                                temp.append(position)
                                self.tableau_proba[position.x, position.y] += 1
                for t in temp:
                    self.modifie_grille(plateau2, t, 0)

    # supprime une position dans la liste position
    def supprimer_position(self, position, liste_position):
        valeur = 0
        for i in range(len(liste_position)):
            if liste_position[i] == position:
                valeur = i
                break
        liste_position.pop(valeur)

    # supprime un bateau dans la liste bateau
    def supprimer_bateau(self, bateau, bateaux):
        valeur = 0
        for i in range(len(bateaux)):
            if bateaux[i] == bateau:
                valeur = i
                break
        bateaux.pop(valeur)

    # diminue d'une vie du bateau donné en parametre
    def diminue_vie(self, id_bateau):
        # Pop utilise les indices on utilise alors range
        for i in range(len(self.bateaux)):
            if self.bateaux[i].identifiant == id_bateau:
                if self.bateaux[i].vie > 0:
                    self.bateaux[i].vie += -1

    # augmente d'une vie du bateau donné en parametre
    def augmenter_vie(self, id_bateau):
        # Pop utilise les indices on utilise alors range
        for i in range(len(self.bateaux)):
            if self.bateaux[i].identifiant == id_bateau:
                self.bateaux[i].vie += 1

    # modifie le plateau
    def modifie_plateau(self, position):
        if 0 <= position.x < len(self.plateau) and 0 <= position.y < len(self.plateau[0]):
            self.plateau[position.x, position.y] = position.identifiant

    # modifie la grille
    def modifie_grille(self, plateau, position, valeur):
        if 0 <= position.x < len(plateau) and 0 <= position.y < len(plateau[0]):
            plateau[position.x, position.y] = valeur

    # Supprime les bateaux qui ne possedent plus de vie
    def bateau_vivant(self):
        indice = -1
        for i in range(len(self.bateaux)):
            if self.bateaux[i].vie <= 0:
                indice = i

        if indice >= 0:
            self.bateaux.pop(indice)

    # Fonction qui retourne le bateau d'identifiant id_bateau
    def retourne_bateau(self, bateaux, id_bateau):
        for bateau in bateaux:
            if bateau.identifiant == id_bateau:
                return bateau
        return None

    # retourne true si la partie est finie
    def victoire(self):
        self.bateau_vivant()
        return len(self.bateaux) <= 0

    # Retourne un tableau vide
    def init_tableau(self, largeur, longeur):
        return np.zeros([largeur, longeur], dtype=int)

    # reconstitue le plateau
    # indispensable pour jouer les memes grilles avec les differentes strategie
    def reset(self):

        self.compteur = 0
        self.plateau = copy.deepcopy(self.plateau_ref)
        self.bateaux = copy.deepcopy(self.bateaux_ref)
        self.position_jouer = []
        self.position_toucher = []
