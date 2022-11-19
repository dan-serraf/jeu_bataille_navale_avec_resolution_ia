import matplotlib.pyplot as plt
from Bataille import *
from Joueur import *



#Retourne une liste avec les coordonnes des abscisses 
def calcul_donne_abscisse(borne_inf, borne_sup, pas):
    liste_abscisse = []
    for i in range(borne_inf, borne_sup, pas):
        liste_abscisse.append(i)

    return liste_abscisse



#Retourne une liste avec les coordonnes des ordonnées
#Calcul le nombre de coup moyens en fonction du nombre d'iteration
def calcul_donne_ordonne(liste_abscisse, liste_bateau_id, liste_bateaux_taille, largeur, longeur, option):
    liste_ordonne = []
    bateaux = genere_bateaux(liste_bateau_id, liste_bateaux_taille)
    plateau = genere_grille(largeur, longeur, bateaux)
    bataille = Bataille(plateau, bateaux)
    joueur = Joueur((0, 0))
    liste_position = joueur.liste_position(largeur, longeur)

    for nombre_iteration in liste_abscisse:
        temp = []
        somme = 0
        for i in range(nombre_iteration):
            liste_position2 = copy.deepcopy(liste_position)
            random.shuffle(liste_position2)
            if option == 1:
                temp.append(joueur.joue_aleatoire(bataille, liste_position2))
            elif option == 2:
                temp.append(joueur.joue_heuristique(bataille, liste_position2))
            elif option == 3:
                temp.append(joueur.joue_probabiliste(bataille, liste_position2))
            else:
                temp.append(joueur.joue_monte_carlo(bataille, liste_position2))

        for t in temp:
            somme += t
        liste_ordonne.append(somme / (len(temp)))
        bataille.reset()

    return liste_ordonne

#Retourne une liste avec les coordonnes des abscisses et des ordonnées pour crée le graphe
def calcule_tableau(borne_inf, borne_sup, pas, liste_bateau_id, liste_bateaux_taille, largeur, longeur, option):
    liste_abscisse = calcul_donne_abscisse(borne_inf, borne_sup, pas)
    liste_ordonne = calcul_donne_ordonne(liste_abscisse, liste_bateau_id, liste_bateaux_taille, largeur, longeur,
                                         option)
    return [liste_abscisse, liste_ordonne]

#Fonction qui permet de dessiner un graphe avec matplotlib
def dessine_graphe(liste_abscisse, liste_ordonne, couleur, nom_graphe, nom_abscisse, nom_ordonne):
    plt.title(nom_graphe)
    plt.ylabel(nom_abscisse)
    plt.xlabel(nom_ordonne)
    plt.plot(liste_abscisse, liste_ordonne, color=couleur, linewidth=3)
    plt.show()
