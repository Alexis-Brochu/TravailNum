#Travail numérique ÉlectroMagnétisme H2024
#William Boissonneault (537 xxx xxx)
#Alexis Gagné-Brochu (537 xxx xxx)
#2024-04-26

import numpy as np
import matplotlib.pyplot as plt
import fonctions_utiles as fu
import time


#Nous travaillerons toujours en m, le tout sera transformé en mm lors de l'affichage
#des figures

#INITIALISATION
start_time = time.time()    #Commence chronomètre
h = 0.0001   #agit comme ''Résolution'' de relaxation 


#Comme 

def Construire_Matrice_CF(){
    """Cette fonction crée une matrice numpy 2D avec la géométrie du problème,
    La valeur de condition est inscrite, si le noeud n'est pas fixe, la valeur False
    est inscrite"""

    return Matrice_CF
}

def Initialisation_Vactuel(Matrice_CF){
    """Cette fonction crée la première matrice numpy 2D du potentiel actuel,
    Les valeurs de potentiel en tout point est mise"""



    return V_début
}

def Relaxation_simple(V_actuel, Matrice_CF){
    """Cette fonction effectue une étape de Relaxation et retourne la nouvelle
    matrice du potentiel actuel et un indice du changements effectuté"""
    
    M_Vactuel_gauche = V_actuel[::]
    M_Vactuel_droite = V_actuel[::]
    M_Vactuel_haut = V_actuel[::]
    M_Vactuel_bas = V_actuel[::]

    #TODO utiliser vraie mathématique
    V_nouveaux = 0.25 * (M_Vactuel_gauche + M_Vactuel_droite + M_Vactuel_haut + M_Vactuel_bas) + Facteur_cylindrique

    #Replacemnt dans condtions frontières
    V_nouveaux = V_nouveaux OPERATION Matrice_CF

    #Indice de changement pour condition de fin
    Indice_changement = np.average(V_actuel) - np.average(V_nouveaux)

    return V_nouveaux, Indice_changement
}

def affichage_de_matrice(Matrice_V, nom_fichier=False){
    """Cette fonction affiche la matrice de potentiel passée en entrée
    Utile pour débogger ET pour la production de figure finale"""

    fig = plt.figure(figsize=(12,7), figdpi=300)

    fig.mesh(
        Matrice_V
    )

    if (save){
        fig.savefigure(nom_fichier)
    }
    fig.show()
}

###Operations###

Matrice_CF = Construire_Matrice_CF()

V_actuel = Initialisation_Vactuel()

Relaxation_en_cours = True

i=0
while(Relaxation_en_cours){
    V_nouveaux, Indice_changement = Relaxation_simple(V_actuel, Matrice_CF)

    print(f"Relaxation {i} effectué, indice de changement : {Indice_changement}")
    ###Condition d'arrêts:
    if (Indice_changement < cond_arret){
        Relaxation_en_cours = False
    }
}

print("Programme executé en --- %s seconds ---" % (time.time() - start_time))
affichage_de_matrice(V_actuel, nom_fichier="nom_de_figure")
