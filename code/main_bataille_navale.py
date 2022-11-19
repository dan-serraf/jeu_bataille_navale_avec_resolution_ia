from UtilitaireNumpy import *

test_alea= calcule_tableau(1,100,1,[1,2,3,4,5],[5,4,3,3,2],10,10,1)    
test_heuriss= calcule_tableau(1,100,1,[1,2,3,4,5],[5,4,3,3,2],10,10,2)    
test_proba= calcule_tableau(1,100,5,[1,2,3,4,5],[5,4,3,3,2],10,10,3)
test_monte_carlo= calcule_tableau(1,2,1,[1,2,3,4,5],[5,4,3,3,2],10,10,4,100)

dessine_graphe(test_alea[0],test_alea[1],'lightgreen',"Tirage aleatoire","Nombre de tire moyens","Nombre d'itérations")
dessine_graphe(test_heuriss[0],test_heuriss[1],'lightgreen',"Tirage heuristique","Nombre de tire moyens","Nombre d'itérations")
dessine_graphe(test_proba[0],test_proba[1],'lightgreen',"Tirage probabiliste","Nombre de tire moyens","Nombre d'itérations")
dessine_graphe(test_monte_carlo[0],test_monte_carlo[1],'lightgreen',"Tirage Monte Carlo","Nombre de tire moyens","Nombre d'itérations")



